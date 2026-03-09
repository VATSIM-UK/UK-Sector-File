#!/usr/bin/env python3
"""
Parse AIXM XML sector data and extract to Euroscope format.
Converts flight level limits from FL to feet (FL * 100).
Writes sectors to ARTCC and Sector Boundaries folders.
"""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re


class SectorParser:
    """Parse AIXM XML sector data and convert to Euroscope format."""
    
    def __init__(self, xml_file: str):
        """Initialize parser with XML file path."""
        self.xml_file = xml_file
        self.namespaces = {
            'aixm': 'http://www.aixm.aero/schema/5.1',
            'gml': 'http://www.opengis.net/gml/3.2',
            'message': 'http://www.aixm.aero/schema/5.1/message',
            'gmd': 'http://www.isotc211.org/2005/gmd',
            'gco': 'http://www.isotc211.org/2005/gco',
        }
        self.tree = None
        self.root = None
        
    def parse(self) -> None:
        """Parse the XML file."""
        try:
            self.tree = ET.parse(self.xml_file)
            self.root = self.tree.getroot()
            print(f"Successfully parsed {self.xml_file}")
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            raise
    
    def fl_to_feet(self, fl: str) -> int:
        """Convert flight level to feet."""
        try:
            return int(fl) * 100
        except (ValueError, TypeError):
            return 0
    
    def decimal_to_dms(self, decimal: float, is_latitude: bool = True) -> str:
        """Convert decimal degrees to DMS format: N061.00.00.000"""
        is_negative = decimal < 0
        decimal = abs(decimal)
        
        degrees = int(decimal)
        minutes_decimal = (decimal - degrees) * 60
        minutes = int(minutes_decimal)
        seconds = (minutes_decimal - minutes) * 60
        
        if is_latitude:
            direction = 'S' if is_negative else 'N'
        else:
            direction = 'W' if is_negative else 'E'
        
        return f"{direction}{degrees:03d}.{minutes:02d}.{seconds:06.3f}"
    
    def extract_coordinates(self, airspace_volume) -> List[Tuple[float, float]]:
        """Extract lat/lon coordinates from airspace volume."""
        coordinates = []
        
        # Navigate to the GeodesicString with points
        horizontal_proj = airspace_volume.find('.//aixm:horizontalProjection', self.namespaces)
        if horizontal_proj is None:
            return coordinates
            
        for point in horizontal_proj.findall('.//aixm:Point', self.namespaces):
            pos = point.find('gml:pos', self.namespaces)
            if pos is not None and pos.text:
                try:
                    lat, lon = pos.text.strip().split()
                    coordinates.append((float(lat), float(lon)))
                except ValueError:
                    continue
        
        return coordinates
    
    def extract_sectors(self) -> List[Dict]:
        """Extract all sectors from the XML."""
        sectors = []
        
        # Find all Airspace elements
        for airspace in self.root.findall('.//aixm:Airspace', self.namespaces):
            sector_info = self._extract_sector_info(airspace)
            if sector_info:
                sectors.append(sector_info)
        
        return sectors
    
    def _extract_sector_info(self, airspace) -> Optional[Dict]:
        """Extract information from a single airspace element."""
        # Get the AirspaceTimeSlice
        timeslice = airspace.find('.//aixm:AirspaceTimeSlice', self.namespaces)
        if timeslice is None:
            return None
        
        # Extract basic information
        designator = timeslice.findtext('aixm:designator', '', self.namespaces)
        name = timeslice.findtext('aixm:name', '', self.namespaces)
        local_type = timeslice.findtext('aixm:localType', '', self.namespaces)
        
        # Skip if no name
        if not name:
            return None
        
        # Extract altitude limits
        airspace_volume = timeslice.find('.//aixm:AirspaceVolume', self.namespaces)
        if airspace_volume is None:
            return None
        
        upper_limit_elem = airspace_volume.find('aixm:upperLimit', self.namespaces)
        lower_limit_elem = airspace_volume.find('aixm:lowerLimit', self.namespaces)
        
        upper_limit_fl = upper_limit_elem.text if upper_limit_elem is not None else "0"
        lower_limit_fl = lower_limit_elem.text if lower_limit_elem is not None else "0"
        
        upper_feet = self.fl_to_feet(upper_limit_fl)
        lower_feet = self.fl_to_feet(lower_limit_fl)
        
        # Extract coordinates
        coordinates = self.extract_coordinates(airspace_volume)
        
        return {
            'designator': designator,
            'name': name,
            'type': local_type,
            'upper_fl': upper_limit_fl,
            'lower_fl': lower_limit_fl,
            'upper_feet': upper_feet,
            'lower_feet': lower_feet,
            'coordinates': coordinates,
        }
    
    def get_artcc_category(self, sector: Dict) -> str:
        """Determine ARTCC category (High/Low) based on sector type."""
        sector_type = sector['type'].upper()
        
        if 'PCUA' in sector_type or 'UPPER' in sector_type:
            return 'High'
        else:
            return 'Low'
    
    def _content_changed(self, filepath: Path, new_content: str) -> bool:
        """Check if file content has changed."""
        if not filepath.exists():
            return True
        
        try:
            with open(filepath, 'r') as f:
                existing_content = f.read()
            return existing_content != new_content
        except Exception:
            return True
    
    def write_to_artcc_files(self, sectors: List[Dict], base_dir: Path) -> None:
        """Write sectors to ARTCC High/Low files organized by FIR."""
        artcc_dir = base_dir / 'ARTCC'
        
        # Group sectors by category and FIR
        high_sectors = {}
        low_sectors = {}
        
        for sector in sectors:
            category = self.get_artcc_category(sector)
            # Use designator (FIR code) as key, or a default
            fir = sector['designator'] or 'EGTT'
            
            if category == 'High':
                if fir not in high_sectors:
                    high_sectors[fir] = []
                high_sectors[fir].append(sector)
            else:
                if fir not in low_sectors:
                    low_sectors[fir] = []
                low_sectors[fir].append(sector)
        
        # Write high sectors
        if high_sectors:
            self._write_artcc_category(artcc_dir / 'High', high_sectors)
        
        # Write low sectors
        if low_sectors:
            self._write_artcc_category(artcc_dir / 'Low', low_sectors)
    
    def _write_artcc_category(self, output_dir: Path, fir_sectors: Dict) -> None:
        """Write ARTCC files for a specific category."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for fir, sectors in fir_sectors.items():
            # Create filename from sector names
            for sector in sectors:
                filename = f"{fir} {sector['name']}.txt"
                filepath = output_dir / filename
                
                lines = []
                lines.append(f";{sector['name']} FL{sector['lower_fl']}-FL{sector['upper_fl']}")
                
                # Add sector lines
                if sector['coordinates']:
                    for i in range(len(sector['coordinates']) - 1):
                        lat1, lon1 = sector['coordinates'][i]
                        lat2, lon2 = sector['coordinates'][i + 1]
                        
                        lat1_dms = self.decimal_to_dms(lat1, True)
                        lon1_dms = self.decimal_to_dms(lon1, False)
                        lat2_dms = self.decimal_to_dms(lat2, True)
                        lon2_dms = self.decimal_to_dms(lon2, False)
                        
                        line = f"{fir} {sector['name']} {lat1_dms} {lon1_dms} {lat2_dms} {lon2_dms}"
                        lines.append(line)
                
                # Check if content changed before writing
                new_content = '\n'.join(lines)
                if self._content_changed(filepath, new_content):
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"  Updated: {filepath}")
                else:
                    print(f"  Unchanged: {filepath}")
    
    def write_to_sector_boundaries(self, sectors: List[Dict], base_dir: Path) -> None:
        """Write sectors to Sector Boundaries folder."""
        sb_dir = base_dir / 'Sector Boundaries'
        sb_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a file for each unique sector group or write combined file
        for sector in sectors:
            # Use a more descriptive filename based on sector name and altitude
            filename = f"Lines - {sector['name']}.txt"
            filepath = sb_dir / filename
            
            lines = []
            
            # Sector line definition
            sector_friendly_name = sector['name'].replace('_', ' ')
            lines.append(f"SECTORLINE:{sector_friendly_name}")
            
            # Display definitions (for left/right neighbor relationships)
            lines.append(f"DISPLAY:{sector_friendly_name}:{sector_friendly_name}:{sector_friendly_name}")
            lines.append(f"DISPLAY:{sector_friendly_name}:{sector_friendly_name}:{sector_friendly_name}")
            
            # Coordinates in DMS format
            if sector['coordinates']:
                for lat, lon in sector['coordinates']:
                    lat_dms = self.decimal_to_dms(lat, True)
                    lon_dms = self.decimal_to_dms(lon, False)
                    lines.append(f"COORD:{lat_dms}:{lon_dms}")
            
            lines.append("")  # Blank line at end
            
            # Check if content changed before writing
            new_content = '\n'.join(lines)
            if self._content_changed(filepath, new_content):
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"  Updated: {filepath}")
            else:
                print(f"  Unchanged: {filepath}")


    def write_coordinates_to_root(self, sectors: List[Dict], base_dir: Path) -> None:
        """Write all coordinates to a root folder as CSV."""
        coords_dir = base_dir / "Sector Coordinates"
        coords_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a combined CSV file with all coordinates
        filepath = coords_dir / "all_sectors_coordinates.csv"
        
        lines = ["Sector,Latitude,Longitude,Latitude_DMS,Longitude_DMS"]
        
        for sector in sectors:
            if sector['coordinates']:
                for lat, lon in sector['coordinates']:
                    lat_dms = self.decimal_to_dms(lat, True)
                    lon_dms = self.decimal_to_dms(lon, False)
                    line = f"{sector['name']},{lat:.6f},{lon:.6f},{lat_dms},{lon_dms}"
                    lines.append(line)
        
        new_content = '\n'.join(lines)
        if self._content_changed(filepath, new_content):
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"  Updated: {filepath}")
        else:
            print(f"  Unchanged: {filepath}")
        
        # Create individual sector files with coordinates
        for sector in sectors:
            if sector['coordinates']:
                filename = f"{sector['name']}_coordinates.txt"
                filepath = coords_dir / filename
                
                lines = [f"Sector: {sector['name']}"]
                lines.append(f"Designator: {sector['designator']}")
                lines.append(f"Type: {sector['type']}")
                lines.append(f"Altitude: FL{sector['lower_fl']} - FL{sector['upper_fl']}")
                lines.append("")
                lines.append("Coordinates (Decimal):")
                
                for lat, lon in sector['coordinates']:
                    lines.append(f"  {lat:.6f}, {lon:.6f}")
                
                lines.append("")
                lines.append("Coordinates (DMS):")
                
                for lat, lon in sector['coordinates']:
                    lat_dms = self.decimal_to_dms(lat, True)
                    lon_dms = self.decimal_to_dms(lon, False)
                    lines.append(f"  {lat_dms} {lon_dms}")
                
                lines.append("")
                
                new_content = '\n'.join(lines)
                if self._content_changed(filepath, new_content):
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"  Updated: {filepath}")


def main():
    """Main entry point."""
    import sys
    
    # Use DIFF file by default, or FULL file if specified
    xml_file = Path(__file__).parent / "EG_LAC_PC_SECTOR_DS_20260319_XML" / "EG_LAC_PC_SECTOR_DS_DIFF_DELTA_20260319.xml"
    
    if len(sys.argv) > 1:
        xml_file = Path(sys.argv[1])
    
    if not xml_file.exists():
        print(f"Error: XML file not found: {xml_file}")
        sys.exit(1)
    
    print(f"Parsing sectors from: {xml_file}")
    parser = SectorParser(str(xml_file))
    parser.parse()
    
    sectors = parser.extract_sectors()
    print(f"Found {len(sectors)} sectors\n")
    
    # Get base directory (workspace root)
    base_dir = xml_file.parent.parent
    
    # Write all coordinates to root folder
    print("Writing coordinates to root folder:")
    parser.write_coordinates_to_root(sectors, base_dir)
    
    print("\nDone!")


if __name__ == "__main__":
    main()
