def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    # Dynamically determine leading empty header cells
    leading_empty_cols = 0
    for col in multi_headers[0]:
        if col.strip() == "":
            leading_empty_cols += 1
        else:
            break

    # Create headers row-by-row
    for level in range(num_levels):
        row = []
        col_idx = 0
        while col_idx < num_columns:
            header = multi_headers[level][col_idx]

            # Handle empty leading cells at the top level
            if level == 0 and col_idx < leading_empty_cols:
                row.append("")  # Add empty string to keep cell in layout
                # Explicitly remove borders and background
                header_styles.append(('LINEBEFORE', (col_idx, level), (col_idx, level), 0, colors.white))
                header_styles.append(('LINEABOVE', (col_idx, level), (col_idx, level), 0, colors.white))
                header_styles.append(('LINEBELOW', (col_idx, level), (col_idx, level), 0, colors.white))
                header_styles.append(('BACKGROUND', (col_idx, level), (col_idx, level), colors.white))
                col_idx += 1
                continue

            # Calculate horizontal span for repeated headers
            span_count = 1
            while (col_idx + span_count < num_columns and
                   multi_headers[level][col_idx + span_count] == header):
                span_count += 1

            row.append(Paragraph(f"<b>{header}</b>", custom_style))

            column_info = report_column_info[col_idx] if col_idx < len(report_column_info) else {}
            column_group = column_info.get('group', 'Group1')
            bg_color = group_colors.get(column_group, '#DCDCDC')

            # Apply normal header styles
            header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
            header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
            header_styles.append(('VALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'MIDDLE'))
            header_styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.black))

            if span_count > 1:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            col_idx += span_count

        table_data.append(row)

    # Populate data rows
    for _, row_data in dataframe.iterrows():
        data_row = [Paragraph(str(row_data[col["column"]]), custom_style) for col in report_column_info]
        table_data.append(data_row)

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
