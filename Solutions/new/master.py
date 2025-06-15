def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    # Detect how many leading empty columns exist in level 0 (top header row)
    empty_leading_cols = 0
    for col in multi_headers[0]:
        if col.strip() == "":
            empty_leading_cols += 1
        else:
            break

    # 1. Multi-level header rendering
    for level in range(num_levels):
        row = []
        col_idx = 0

        while col_idx < num_columns:
            header = multi_headers[level][col_idx]

            # Handle blank cells at the beginning: skip styling/borders
            if col_idx < empty_leading_cols:
                row.append("")  # blank cell with no formatting
                col_idx += 1
                continue

            # Count how many times this header spans to the right
            span_count = 1
            while (col_idx + span_count < num_columns and
                   multi_headers[level][col_idx + span_count] == header):
                span_count += 1

            # Render actual header content
            cell = Paragraph(f"<b>{header}</b>", custom_style)
            row.append(cell)

            # Background styling and span
            group_colors_config = self.config["reports"][0]["topics"][0]["table_style"]["group_colors"]
            column_info = report_column_info[col_idx] if col_idx < len(report_column_info) else {}
            column_group = column_info.get("group", "Group1")
            bg_color = group_colors_config.get(column_group, "#FFFFFF")

            header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
            header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
            header_styles.append(('VALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'MIDDLE'))
            header_styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.black))

            if span_count > 1:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            col_idx += span_count

        table_data.append(row)

    # 2. Data rows
    for _, row in dataframe.iterrows():
        data_row = [Paragraph(str(row[col["column"]]), custom_style) for col in report_column_info]
        table_data.append(data_row)

    return table_data, header_styles
