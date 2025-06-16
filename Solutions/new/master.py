def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    white_text_style = ParagraphStyle(
        name="WhiteHeaderStyle",
        parent=custom_style,
        textColor=colors.white,
        alignment=1,  # center
    )

    black_text_style = ParagraphStyle(
        name="BlackHeaderStyle",
        parent=custom_style,
        textColor=colors.white,
        alignment=1,  # center
    )

    for level in range(num_levels):
        row = []
        styles = []
        col_idx = 0

        while col_idx < num_columns:
            header = multi_headers[level][col_idx]
            span_count = 1
            row.append('')  # prepare to fill later

            # Count how many columns to merge
            while (
                col_idx + span_count < num_columns and
                multi_headers[level][col_idx + span_count] == header
            ):
                span_count += 1
                row.append('')

            # Blank cell, no style
            if level == 0 and header == '':
                row[col_idx] = ''
            else:
                if level == 0:
                    row[col_idx] = Paragraph(f"<b>{header}</b>", white_text_style)
                    styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor('#1372be')))
                else:
                    row[col_idx] = Paragraph(f"<b>{header}</b>", black_text_style)
                    styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor('#1f2c42')))

                styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.white))
                styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))

            if span_count > 1:
                styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            col_idx += span_count

        table_data.append(row)
        header_styles.extend(styles)

    # Add border and grid for headers and table
    total_rows = len(table_data)
    header_styles.append(('GRID', (0, 0), (num_columns - 1, total_rows - 1), 0.75, colors.black))
    header_styles.append(('BOX', (0, 0), (num_columns - 1, total_rows - 1), 1.0, colors.black))

    return table_data, header_styles
