from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    empty_column = 0
    for col in multi_headers[0]:
        if col == "":
            empty_column += 1
        else:
            break

    for level in range(num_levels):
        headers = multi_headers[level]
        row = []
        styles = []
        col_idx = 0

        while col_idx < num_columns:
            header = headers[col_idx]
            span_count = 1

            # Skip empty top-level headers before meaningful ones
            if col_idx < empty_column and level < num_levels - 1:
                row.append('')
                col_idx += 1
                continue

            # Count span (how many columns have the same header)
            while (col_idx + span_count < num_columns and
                   headers[col_idx + span_count] == header):
                span_count += 1

            while len(row) <= col_idx:
                row.append('')

            row[col_idx] = Paragraph(f"<b>{header}</b>", custom_style)

            # Background colors for first and second header levels
            if level == 0:
                bg_color = colors.HexColor("#A4BFEF")  # light blue
                if header.strip() != "":
                    styles.append(('LINEABOVE', (col_idx, level), (col_idx + span_count - 1, level), 0.5, colors.black))
            else:
                bg_color = colors.HexColor("#C9C3E6")  # light purple

            styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), bg_color))

            # Span
            if span_count > 1:
                styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            # Grid and alignment
            styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
            styles.append(('VALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'MIDDLE'))

            col_idx += span_count

        table_data.append(row)
        header_styles.extend(styles)

    # Now the data rows
    for _, data_row in dataframe.iterrows():
        row = [Paragraph(str(data_row.get(col['column'], '')), custom_style) for col in report_column_info]
        table_data.append(row)

    return table_data, header_styles


def create_table_style(self, style_config):
    style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#000000")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, 1), 3),
        ('RIGHTPADDING', (0, 0), (-1, 1), 3),
        ('TOPPADDING', (0, 0), (-1, 1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, 1), 3),
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Remove the top border for the first header row in these columns
    no_top_border_columns = [0, 1, 2, 3, 4]  # adjust based on your column positions
    for col in no_top_border_columns:
        style.add('LINEABOVE', (col, 0), (col, 0), 0, colors.white)

    return style

def create_table_style(self, style_config):
    style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#000000")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, 1), 3),
        ('RIGHTPADDING', (0, 0), (-1, 1), 3),
        ('TOPPADDING', (0, 0), (-1, 1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, 1), 3),
        ('GRID', (0, 0), (-1, -1), 0.1, colors.gray),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
    ])

    # Dynamically remove top border for specified columns
    no_top_border_cols = style_config.get("no_top_border_columns", [])
    for col in no_top_border_cols:
        style.add('LINEABOVE', (col, 0), (col, 0), 0, colors.white)

    return style
