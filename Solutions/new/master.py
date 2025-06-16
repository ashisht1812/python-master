# Patch for prepare_table_data and table styling to remove extra lines from first-level headers
# and maintain clean visual structure

from reportlab.platypus import Paragraph, TableStyle
from reportlab.lib import colors


def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    # Find leading empty header cells
    empty_column = 0
    for col in multi_headers[0]:
        if col == '':
            empty_column += 1
        else:
            break

    for level in range(num_levels):
        headers = multi_headers[level]
        row = []
        col_idx = 0
        while col_idx < num_columns:
            header = headers[col_idx]
            span_count = 1

            if col_idx < empty_column and level < num_levels - 1:
                row.append('')
                col_idx += 1
                continue

            while col_idx + span_count < num_columns and headers[col_idx + span_count] == header:
                span_count += 1

            while len(row) <= col_idx:
                row.append('')

            row[col_idx] = Paragraph(f"<b>{header}</b>", custom_style)

            # Add SPAN and BACKGROUND styles
            if span_count > 1:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            # Only apply background for non-empty cells
            if header != '':
                header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor("#DDE1F5")))
                header_styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.black))
                header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))

            col_idx += span_count

        table_data.append(row)

    return table_data, header_styles


def create_table_style(self, style_config, no_top_border_columns=[]):
    base = [
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
        ('GRID', (0, 0), (-1, -1), 0.1, colors.HexColor("#D3D3D3")),
    ]

    for col in no_top_border_columns:
        base.append(('LINEABOVE', (col, 0), (col, 0), 0, colors.white))

    return TableStyle(base)
