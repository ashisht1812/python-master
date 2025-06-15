def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    report_config = self.config.get("reports", [{}])[0]
    columns_config = report_config.get("columns", [])
    no_top_border_columns = report_config.get("no_top_border_columns", [])

    for level in range(num_levels):
        headers = multi_headers[level]
        row = []
        styles = []
        col_idx = 0

        while col_idx < num_columns:
            header = headers[col_idx]
            span_count = 1

            # Count how many times the header is repeated
            while (col_idx + span_count < num_columns) and (headers[col_idx + span_count] == header):
                span_count += 1

            # Append header text
            row.append(Paragraph(f"<b>{header}</b>", custom_style))

            # Set background color based on header level
            if level == 0:
                bg_color = colors.HexColor("#DDEBF7")  # light purple for first-level
            else:
                bg_color = colors.HexColor("#B4C6E7")  # blue for second-level

            # Apply span
            if span_count > 1:
                styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            # Apply background
            styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), bg_color))
            styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.white))
            styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))

            # Handle removal of top border for certain columns on second-level only
            if level == 1:
                col_header = header.strip()
                if col_header in no_top_border_columns:
                    styles.append(('LINEABOVE', (col_idx, level), (col_idx + span_count - 1, level), 0.0, colors.white))

            col_idx += span_count

        table_data.append(row)
        header_styles.extend(styles)

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
