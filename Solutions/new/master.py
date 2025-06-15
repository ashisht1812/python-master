def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[0])

    # Find first non-empty cell in level 0 to start drawing real headers
    first_group_idx = next((i for i, h in enumerate(multi_headers[0]) if h.strip()), 0)

    for level in range(num_levels):
        row = []
        col_idx = 0
        while col_idx < num_columns:
            header = multi_headers[level][col_idx]

            # 🛑 Skip first-level empty cells before actual headers
            if level == 0 and col_idx < first_group_idx:
                row.append("")  # placeholder to align columns
                col_idx += 1
                continue

            # Count how many columns this header should span
            span_count = 1
            while (col_idx + span_count < num_columns and
                   multi_headers[level][col_idx + span_count] == header):
                span_count += 1

            cell = Paragraph(f"<b>{header}</b>", custom_style)
            row.append(cell)

            # Get group info for color
            column_info = report_column_info[col_idx] if col_idx < len(report_column_info) else {}
            column_group = column_info.get("group", "Group1")
            bg_color = group_colors.get(column_group, "#DCDCDC")

            # Style header cell
            header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
            header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
            header_styles.append(('VALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'MIDDLE'))
            header_styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.black))
            if span_count > 1:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            col_idx += span_count

        table_data.append(row)

    # ➕ Add the actual data rows
    for _, row in dataframe.iterrows():
        data_row = [Paragraph(str(row[col["column"]]), custom_style) for col in report_column_info]
        table_data.append(data_row)

    return table_data, header_styles
