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

    # Process headers for each level
    for level in range(num_levels):
        headers = multi_headers[level]
        row = []
        col_idx = 0

        while col_idx < num_columns:
            header = headers[col_idx]
            span_count = 1

            if col_idx < empty_column and level < num_levels - 1:
                row.append("")
                col_idx += 1
                continue

            while col_idx + span_count < num_columns and headers[col_idx + span_count] == header:
                span_count += 1

            while len(row) <= col_idx:
                row.append("")

            row[col_idx] = Paragraph(f"<b>{header}</b>", custom_style)

            if span_count > 1:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            report_config = self.config.get("reports", [{}])[0]
            columns_config = report_config.get("columns", [])
            column_config = next((col for col in columns_config if col.get("header") == header), None)
            bg_color = column_config.get("bg_color") if column_config else None

            if level == 0 and header == "":
                # Do not apply background or borders for blank top-level headers
                pass
            elif level == 0:
                header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color or "#d3d3d3")))
                header_styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.white))
                header_styles.append(('FONTNAME', (col_idx, level), (col_idx + span_count - 1, level), 'Helvetica-Bold'))
                header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
            else:
                header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color or "#e6e6f5")))
                header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))

            col_idx += span_count

        table_data.append(row)

    return table_data, header_styles

def create_table_style(self, style_config, no_top_border_columns=[]):
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
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor("#d3d3d3")),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.HexColor("#d3d3d3")),
    ])

    # Remove TOP border for columns listed in no_top_border_columns
    for col_idx in no_top_border_columns:
        style.add('LINEABOVE', (col_idx, 0), (col_idx, 0), 0, colors.white)
        style.add('BOX', (col_idx, 0), (col_idx, 0), 0, colors.white)

    return style
