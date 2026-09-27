import argparse
import sys
from pathlib import Path

from lxml import etree


KML_NS = {
    "kml": "http://www.opengis.net/kml/2.2"
}

REGION_NAME = "Heathrow"
KML_DEFAULT_COLOR = "ffffffff"


def decimal_to_dms(value, positive, negative, decimals=3):
    """Convert decimal degrees to N051.28.33.761-style format."""

    direction = positive if value >= 0 else negative
    value = abs(value)

    degrees = int(value)
    minutes_float = (value - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60

    return f"{direction}{degrees:03d}.{minutes:02d}.{seconds:0{3+decimals}.{decimals}f}"


def format_coordinate(lon, lat):
    lat_text = decimal_to_dms(lat, "N", "S")
    lon_text = decimal_to_dms(lon, "E", "W")

    return f"{lat_text} {lon_text}"


def parse_coordinates(text):
    """Convert KML coordinate string into Geo coordinate strings."""

    coordinates = []

    for item in text.split():
        lon, lat, *_ = item.split(",")

        coordinates.append(
            format_coordinate(float(lon), float(lat))
        )

    return coordinates


def segments(points):
    """Convert points into pairs suitable for Geo.txt."""

    return list(zip(points, points[1:]))


def kml_color_to_rgb(color):
    """Convert KML aabbggrr color to EuroScope's packed decimal format."""

    color = color.strip().lstrip("#")
    if len(color) != 8:
        raise ValueError(f"Expected an 8-digit KML color, got {color!r}")

    red = int(color[6:8], 16)
    green = int(color[4:6], 16)
    blue = int(color[2:4], 16)
    return red + green * 256 + blue * 65536


def resolve_style(placemark, styles, style_maps):
    style = placemark.find("kml:Style", namespaces=KML_NS)
    if style is not None:
        return style

    style_url = placemark.findtext("kml:styleUrl", namespaces=KML_NS)
    visited = set()
    while style_url:
        style_id = style_url.rsplit("#", 1)[-1]
        if style_id in visited:
            raise ValueError(f"Cyclic KML style map: {style_url}")
        visited.add(style_id)

        if style_id in styles:
            return styles[style_id]

        style_map = style_maps.get(style_id)
        if style_map is None:
            break

        style_url = style_map.xpath(
            "string(kml:Pair[kml:key='normal']/kml:styleUrl)",
            namespaces=KML_NS,
        )

    raise ValueError(f"Unable to resolve KML style: {style_url!r}")


def get_style_color(placemark, style_name, styles, style_maps):
    style = resolve_style(placemark, styles, style_maps)
    color = style.findtext(
        f"kml:{style_name}/kml:color",
        default=KML_DEFAULT_COLOR,
        namespaces=KML_NS,
    )

    return kml_color_to_rgb(color)


def convert_kml(kml_file):

    tree = etree.parse(kml_file)
    styles = {
        style.get("id"): style
        for style in tree.xpath(".//kml:Style[@id]", namespaces=KML_NS)
    }
    style_maps = {
        style_map.get("id"): style_map
        for style_map in tree.xpath(".//kml:StyleMap[@id]", namespaces=KML_NS)
    }

    placemarks = tree.xpath(
        ".//kml:Placemark",
        namespaces=KML_NS
    )

    for placemark in placemarks:

        name = placemark.findtext(
            "kml:name",
            namespaces=KML_NS
        )
        parent = placemark.getparent()
        folder_name = None
        while parent is not None:
            if parent.tag == f"{{{KML_NS['kml']}}}Folder":
                folder_name = parent.findtext("kml:name", namespaces=KML_NS)
                break
            parent = parent.getparent()

        # LineString
        lines = placemark.xpath(
            ".//kml:LineString/kml:coordinates",
            namespaces=KML_NS
        )

        # Polygon
        polygons = placemark.xpath(
            ".//kml:Polygon/kml:outerBoundaryIs/"
            "kml:LinearRing/kml:coordinates",
            namespaces=KML_NS
        )

        for line in lines:
            points = parse_coordinates(line.text)
            color = get_style_color(placemark, "LineStyle", styles, style_maps)
            yield "line", folder_name, name, segments(points), color

        for polygon in polygons:
            points = parse_coordinates(polygon.text)
            color = get_style_color(placemark, "PolyStyle", styles, style_maps)
            yield "polygon", folder_name, name, points, color


def geo_header(kml_file):
    tree = etree.parse(kml_file)
    airport_code = Path(kml_file).stem.upper()
    airport_name = tree.findtext(
        "./kml:Document/kml:Folder/kml:name",
        namespaces=KML_NS,
    )

    if airport_name and airport_name.endswith(" SMR"):
        airport_name = airport_name[:-4]
    if not airport_name:
        airport_name = airport_code

    pseudo_coordinates = (
        "S999.00.00.000 E999.00.00.000 "
        "S999.00.00.000 E999.00.00.000"
    )
    return f"{airport_code} {airport_name:<22} {pseudo_coordinates}"


def write_outputs(kml_file, geo_file, regions_file):
    with open(geo_file, "w", encoding="utf-8") as geo_output, open(
        regions_file, "w", encoding="utf-8"
    ) as regions_output:
        geo_output.write(f"{geo_header(kml_file)}\n")
        last_geo_folder = None
        last_regions_folder = None
        for geometry_type, folder_name, name, geometry, color in convert_kml(kml_file):
            if geometry_type == "line":
                if folder_name != last_geo_folder:
                    if folder_name:
                        geo_output.write(f"\n;{folder_name}\n\n")
                    last_geo_folder = folder_name

                geo_output.write(f";{name}\n")

                for start, end in geometry:
                    geo_output.write(
                        f"{start} {end} {color}\n"
                    )
                continue

            if not geometry:
                continue

            if folder_name != last_regions_folder:
                if folder_name:
                    regions_output.write(f"\n;{folder_name}\n\n")
                last_regions_folder = folder_name

            regions_output.write(
                f";{name}\nREGIONNAME {REGION_NAME}\n"
                f"{color} {geometry[0]}\n"
            )
            for point in geometry[1:]:
                regions_output.write(f"{point}\n")
            regions_output.write("\n")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert an airport KML file to Geo.txt and Regions.txt."
    )
    parser.add_argument("airport", help="four-character airport code, e.g. EGLL")
    args = parser.parse_args(argv)

    airport_code = args.airport.upper()
    if len(airport_code) != 4 or not airport_code.isalnum():
        parser.error("airport must be a four-character alphanumeric code")

    airport_directory = Path(__file__).resolve().parent / airport_code
    kml_file = airport_directory / f"{airport_code}.kml"
    if not kml_file.is_file():
        print(f"Warning: KML file not found: {kml_file}", file=sys.stderr)
        return 1

    write_outputs(
        kml_file,
        airport_directory / "Geo.txt",
        airport_directory / "Regions.txt",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())