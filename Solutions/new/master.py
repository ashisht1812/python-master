def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    # 1. Find the starting column index where headers actually begin (i.e. first non-empty in top-level)
    first_non_empty_idx = next(
        (i for i, val in enumerate(multi_headers[0]) if val.strip() != ""), num_columns
    )

    # 2. Now build multi-level header rows
    for level in range(num_levels):
        row = []
        col_idx = 0
        while col_idx < num_columns:
            header = multi_headers[level][col_idx]
            if col_idx < first_non_empty_idx:
                # Pad empty space — use Spacer or skip appending (no cell borders)
                row.append("")  # Skip rendering this cell entirely
                col_idx += 1
                continue

            # Count how many times this header spans horizontally
            span_count = 1
            while (col_idx + span_count < num_columns and
                   multi_headers[level][col_idx + span_count] == header):
                span_count += 1

            cell = Paragraph(f"<b>{header}</b>", custom_style)
            row.append(cell)

            # Add background and SPAN styles if needed
            header_styles.append(
                ('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor("#DCDCDC"))
            )
            if span_count > 1:
                header_styles.append(
                    ('SPAN', (col_idx, level), (col_idx + span_count - 1, level))
                )

            col_idx += span_count

        table_data.append(row)

    # 3. Add data rows
    for _, row in dataframe.iterrows():
        data_row = [Paragraph(str(row[col["column"]]), custom_style) for col in report_column_info]
        table_data.append(data_row)

    return table_data, header_styles
