def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    # ✅ Step 1: Identify how many leading blank header columns (i.e., from left to first meaningful group)
    empty_column = 0
    for col in multi_headers[0]:
        if col.strip() == "":
            empty_column += 1
        else:
            break  # stop when we hit the first non-empty header

    # ✅ Step 2: Build headers level by level
    for level in range(num_levels):
        headers = multi_headers[level]
        row = []
        col_idx = 0

        while col_idx < num_columns:
            header = headers[col_idx]

            if col_idx < empty_column:
                # Skip rendering (even borders) for early empty columns
                row.append("")  # Keep alignment without rendering actual cells
                col_idx += 1
                continue

            # Count how many times this header repeats (span across)
            span_count = 1
            while (col_idx + span_count < num_columns and
                   headers[col_idx + span_count] == header):
                span_count += 1

            row.append(Paragraph(f"<b>{header}</b>", custom_style))

            # 🔷 Background color based on group config (for top header level)
            report_config = self.config.get("reports", [{}])[0]
            columns_config = report_config.get("topics", [{}])[0].get("table_style", {}).get("columns", [])
            column_config = next((c for c in columns_config if c.get("header") == header), {})
            bg_color = column_config.get("bg_color", "#DCDCDC")

            # Apply styles for span and header
            if span_count > 1:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))
            header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
            header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
            header_styles.append(('VALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'MIDDLE'))
            header_styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.black))

            col_idx += span_count

        table_data.append(row)

    # ✅ Step 3: Add actual data rows
    for _, row in dataframe.iterrows():
        data_row = [Paragraph(str(row[col["column"]]), custom_style) for col in report_column_info]
        table_data.append(data_row)

    return table_data, header_styles
