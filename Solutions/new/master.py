def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    # Add header rows with span calculation
    for level, headers in enumerate(multi_headers):
        row = []
        col_idx = 0
        while col_idx < num_columns:
            header = headers[col_idx]
            span_count = 1

            # Check how many subsequent columns the current header spans
            while (col_idx + span_count < num_columns and 
                   headers[col_idx + span_count] == header):
                span_count += 1

            # Skip empty headers at first level
            if level == 0 and header == '':
                row.extend([''] * span_count)
                col_idx += span_count
                continue

            # Create the header cell
            header_cell = Paragraph(f"<b>{header}</b>", custom_style)
            row.append(header_cell)

            # Determine background color from group_colors or use defaults
            bg_color = group_colors.get(header, "#DDDDFF" if level == 0 else "#EEEEEE")

            # Apply styles conditionally (skip border for empty cells)
            if header:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))
                header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
                header_styles.append(('BOX', (col_idx, level), (col_idx + span_count - 1, level), 0.1, colors.black))
                header_styles.append(('GRID', (col_idx, level), (col_idx + span_count - 1, level), 0.1, colors.gray))
            else:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))
                header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.white))
                # Remove border/grid explicitly
                header_styles.append(('BOX', (col_idx, level), (col_idx + span_count - 1, level), 0, colors.white))
                header_styles.append(('GRID', (col_idx, level), (col_idx + span_count - 1, level), 0, colors.white))

            col_idx += span_count

        table_data.append(row)

    # Append actual data rows from dataframe
    for _, row_data in dataframe.iterrows():
        row = [Paragraph(str(row_data[col['column']]), custom_style) for col in report_column_info]
        table_data.append(row)

    return table_data, header_styles
