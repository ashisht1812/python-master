def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    # Find how many leading columns in the first level header are empty
    empty_column = 0
    for col in multi_headers[0]:
        if col == "":
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

            if col_idx < empty_column and level == 0:
                row.append("")
                col_idx += 1
                continue

            # Count how many times the header is repeated
            while col_idx + span_count < num_columns and headers[col_idx + span_count] == header:
                span_count += 1

            while len(row) <= col_idx:
                row.append("")

            # Render header
            row[col_idx] = Paragraph(f"<b>{header}</b>", custom_style)

            if span_count > 1:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            # Get column config to apply background
            report_config = self.config.get("reports", [{}])[0]
            columns_config = report_config.get("columns", [])
            column_config = next((col for col in columns_config if col.get("header") == header), None)
            bg_color = column_config.get("bg_color") if column_config and "bg_color" in column_config else None

            # Determine default background color
            default_bg = colors.HexColor("#D3D3F3") if level == 0 else colors.HexColor("#DCE6F2")

            # Skip applying background to blank top-level headers
            if not (level == 0 and col_idx < empty_column and header == ""):
                header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), bg_color or default_bg))

            # Style text
            header_styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.white))
            header_styles.append(('FONTNAME', (col_idx, level), (col_idx + span_count - 1, level), 'Helvetica-Bold'))
            header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
            header_styles.append(('VALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'MIDDLE'))

            # Remove left and top borders for empty top-level headers
            if level == 0 and col_idx < empty_column and header == "":
                header_styles.append(('LINEABOVE', (col_idx, level), (col_idx + span_count - 1, level), 0, colors.white))
                header_styles.append(('LINEBEFORE', (col_idx, level), (col_idx + span_count - 1, level), 0, colors.white))

            col_idx += span_count

        table_data.append(row)

    header_styles.append(('GRID', (0, 0), (-1, -1), 0.25, colors.gray))
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
