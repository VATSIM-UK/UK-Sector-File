#!/usr/bin/env python3
"""Convert changed AIXM sectors to ESE-style COORD blocks."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
import re
import xml.etree.ElementTree as ET


NAMESPACES = {
	"aixm": "http://www.aixm.aero/schema/5.1",
	"gml": "http://www.opengis.net/gml/3.2",
}


@dataclass
class SectorBlock:
	name: str
	designator: str
	lower_limit: str
	upper_limit: str
	points: list[tuple[Decimal, Decimal]]


def to_dms(value: Decimal, is_latitude: bool) -> str:
	"""Convert decimal degrees to NDD.MM.SS.mmm / WDDD.MM.SS.mmm."""
	hemisphere = "N" if value >= 0 else "S"
	if not is_latitude:
		hemisphere = "E" if value >= 0 else "W"

	absolute = abs(value)
	total_millis = int(
		(absolute * Decimal(3_600_000)).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
	)
	degrees, remainder = divmod(total_millis, 3_600_000)
	minutes, remainder = divmod(remainder, 60_000)
	seconds, millis = divmod(remainder, 1000)

	degree_width = 2 if is_latitude else 3
	return (
		f"{hemisphere}{degrees:0{degree_width}d}."
		f"{minutes:02d}.{seconds:02d}.{millis:03d}"
	)


def parse_lat_lon(text: str) -> tuple[Decimal, Decimal] | None:
	"""Parse a gml:pos value and keep only EPSG:4326-like ranges."""
	parts = text.strip().split()
	if len(parts) != 2:
		return None

	try:
		lat = Decimal(parts[0])
		lon = Decimal(parts[1])
	except InvalidOperation:
		return None

	if not (Decimal("-90") <= lat <= Decimal("90")):
		return None
	if not (Decimal("-180") <= lon <= Decimal("180")):
		return None
	return lat, lon


def format_limit(value: str, uom: str, reference: str) -> str:
	"""Format vertical limits like SFC, FL255, 4500FT."""
	value = (value or "").strip()
	uom = (uom or "").strip().upper()
	reference = (reference or "").strip().upper()

	if reference == "SFC":
		if not value:
			return "SFC"
		try:
			if Decimal(value) == 0:
				return "SFC"
		except InvalidOperation:
			pass

	if uom == "FL":
		try:
			return f"FL{int(Decimal(value))}"
		except InvalidOperation:
			return f"FL{value}" if value else "FL?"

	if not value:
		return "UNKNOWN"
	if uom:
		return f"{value}{uom}"
	return value


def extract_changed_sector_blocks(xml_path: Path) -> list[SectorBlock]:
	tree = ET.parse(xml_path)
	root = tree.getroot()
	blocks: list[SectorBlock] = []

	for airspace in root.findall(".//aixm:Airspace", NAMESPACES):
		for timeslice in airspace.findall("aixm:timeSlice/aixm:AirspaceTimeSlice", NAMESPACES):
			interpretation = timeslice.findtext("aixm:interpretation", "", NAMESPACES).strip()
			if interpretation and interpretation.upper() != "PERMDELTA":
				continue

			designator = timeslice.findtext("aixm:designator", "", NAMESPACES).strip()
			if not designator:
				continue

			name = timeslice.findtext("aixm:name", "", NAMESPACES).strip() or designator
			volumes = timeslice.findall(".//aixm:AirspaceVolume", NAMESPACES)
			if not volumes:
				continue

			for idx, volume in enumerate(volumes, start=1):
				raw_points = [
					parse_lat_lon(pos.text)
					for pos in volume.findall(".//gml:pos", NAMESPACES)
					if pos.text
				]
				points = [pt for pt in raw_points if pt is not None]
				if not points:
					continue

				upper = volume.find("aixm:upperLimit", NAMESPACES)
				lower = volume.find("aixm:lowerLimit", NAMESPACES)
				upper_ref = volume.findtext("aixm:upperLimitReference", "", NAMESPACES)
				lower_ref = volume.findtext("aixm:lowerLimitReference", "", NAMESPACES)

				upper_limit = format_limit(
					upper.text if upper is not None else "",
					upper.get("uom", "") if upper is not None else "",
					upper_ref,
				)
				lower_limit = format_limit(
					lower.text if lower is not None else "",
					lower.get("uom", "") if lower is not None else "",
					lower_ref,
				)

				block_name = name
				block_designator = designator
				if len(volumes) > 1:
					block_name = f"{name}_PART{idx}"
					block_designator = f"{designator}_P{idx}"

				blocks.append(
					SectorBlock(
						name=block_name,
						designator=block_designator,
						lower_limit=lower_limit,
						upper_limit=upper_limit,
						points=points,
					)
				)

	return blocks


def build_output_text(blocks: list[SectorBlock]) -> str:
	lines: list[str] = []

	for block in blocks:
		lines.append(f"; {block.name} {block.designator}")
		lines.append(
			f"; Limits: lower={block.lower_limit} upper={block.upper_limit}"
		)
		for lat, lon in block.points:
			lines.append(f"COORD:{to_dms(lat, True)}:{to_dms(lon, False)}")
		lines.append("")

	return "\n".join(lines).rstrip() + "\n"


def default_output_for(input_xml: Path, repo_root: Path) -> Path:
	date_match = re.search(r"(\d{8})", input_xml.stem)
	suffix = date_match.group(1) if date_match else "delta"
	return repo_root / "Sector Coordinates" / f"changed_sectors_as_ese_coords_{suffix}.txt"


def main() -> None:
	script_dir = Path(__file__).resolve().parent
	repo_root = script_dir.parent

	parser = argparse.ArgumentParser(
		description="Convert changed sectors from a NATS AIXM delta XML to ESE-style coordinates."
	)
	parser.add_argument(
		"--input",
		type=Path,
		default=repo_root
		/ "EG_LAC_PC_SECTOR_DS_20260319_XML"
		/ "EG_LAC_PC_SECTOR_DS_DIFF_DELTA_20260319.xml",
		help="Path to the delta XML file.",
	)
	parser.add_argument(
		"--output",
		type=Path,
		default=None,
		help="Path for output text file (default: Sector Coordinates/changed_sectors_as_ese_coords_<date>.txt).",
	)
	args = parser.parse_args()

	input_xml = args.input.resolve()
	if not input_xml.exists():
		raise FileNotFoundError(f"Input XML not found: {input_xml}")

	output_path = args.output.resolve() if args.output else default_output_for(input_xml, repo_root)
	output_path.parent.mkdir(parents=True, exist_ok=True)

	blocks = extract_changed_sector_blocks(input_xml)
	output_text = build_output_text(blocks)
	output_path.write_text(output_text, encoding="utf-8")

	print(f"Wrote {len(blocks)} changed sector block(s) to {output_path}")


if __name__ == "__main__":
	main()
