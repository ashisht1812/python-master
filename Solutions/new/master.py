def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    # Dynamically count leading empty cells from the first header level
    leading_empty_cols = 0
    for col in multi_headers[0]:
        if col.strip() == "":
            leading_empty_cols += 1
        else:
            break

    # Process headers level by level
    for level in range(num_levels):
        row = []
        col_idx = 0
        while col_idx < num_columns:
            header = multi_headers[level][col_idx]

            # Skip styling for leading empty cells at first level only
            if level == 0 and col_idx < leading_empty_cols:
                row.append("")  # Alignment placeholder, no borders/styles
                col_idx += 1
                continue

            # Determine span width for repeated headers
            span_count = 1
            while (col_idx + span_count < num_columns and
                   multi_headers[level][col_idx + span_count] == header):
                span_count += 1

            row.append(Paragraph(f"<b>{header}</b>", custom_style))

            # Apply background and span styles
            bg_color = group_colors.get(report_column_info[col_idx].get('group', 'Group1'), '#DCDCDC')

            header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
            header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
            header_styles.append(('VALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'MIDDLE'))
            header_styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.black))

            if span_count > 1:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            col_idx += span_count

        table_data.append(row)

    # Data rows
    for _, row in dataframe.iterrows():
        data_row = [Paragraph(str(row[col["column"]]), custom_style) for col in report_column_info]
        table_data.append(data_row)

    return table_data, header_styles
def create_table_style(self, style_config, multi_level_headers):
    num_levels = len(multi_level_headers)
    num_columns = len(multi_level_headers[0])

    # Count leading empty header cells in the first header row
    leading_empty_cols = next((i for i, val in enumerate(multi_level_headers[0]) if val.strip()), 0)

    styles = [
        ('TEXTCOLOR', (leading_empty_cols, 0), (-1, 0), colors.HexColor("#000000")),
        ('ALIGN', (leading_empty_cols, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (leading_empty_cols, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (leading_empty_cols, 0), (-1, num_levels-1), 0.5, colors.black),
        ('FONTNAME', (leading_empty_cols, 0), (-1, num_levels-1), 'Helvetica-Bold'),
        ('FONTSIZE', (leading_empty_cols, 0), (-1, num_levels-1), 9),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        # Grid and Box starting only from the first visible header cell onwards
        ('GRID', (leading_empty_cols, 0), (-1, -1), 0.1, colors.HexColor('#D3D3D3')),
        ('BOX', (leading_empty_cols, 0), (-1, -1), 0.1, colors.gray),
    ]

    return TableStyle(styles)

def create_table(self, data, style, relative_width, multi_level_headers, additional_styles=None):
    max_width = landscape(letter)
    total_width = max_width[0]
    column_widths = self.calculate_width(relative_width, total_width)

    repeat_rows = len(multi_level_headers)

    table = Table(data, colWidths=column_widths, repeatRows=repeat_rows, splitByRow=True)

    base_style = self.create_table_style(style, multi_level_headers)

    if additional_styles:
        combined_styles = base_style.getCommands() + additional_styles
        table.setStyle(TableStyle(combined_styles))
    else:
        table.setStyle(base_style)

    return table
# some chnages