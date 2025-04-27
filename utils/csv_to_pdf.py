from fpdf import FPDF
import os
import csv


def csv_row_to_pdf(
    input_file,
    output_dir,
    font_name="Arial",
    font_path="/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(font_path):
        raise FileNotFoundError(f"Font file not found: {font_path}")

    try:
        with open(input_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                pdf = FPDF()
                pdf.add_page()
                pdf.add_font(font_name, "", font_path, uni=True)
                pdf.set_font(font_name, size=12)

                for key, value in row.items():
                    pdf.multi_cell(0, 10, f"{key}: {value}")

                output_file = os.path.join(output_dir, f"{row['Title']}.pdf")
                pdf.output(output_file)
                print(f"PDF created: {output_file}")

    except FileNotFoundError:
        print(f"Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Example of available fonts
available_fonts = {
    "DejaVu": "DejaVuSans.ttf",
    "Arial": "/usr/share/fonts/truetype/msttcorefonts/Arial.ttf",
    "Times": "/usr/share/fonts/truetype/msttcorefonts/times.ttf",
    "Courier": "/usr/share/fonts/truetype/msttcorefonts/cour.ttf",
}


def list_available_fonts():
    print("Available fonts:")
    for font_name, font_path in available_fonts.items():
        print(f"{font_name}: {font_path}")
    csv_row_to_pdf("./data/processed/processed_manga.csv", "output_pdfs")


if __name__ == "__main__":
    list_available_fonts()
