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
        alignment=1  # 1 = center
    )

    for level in range(num_levels):
        row = []
        styles = []
        col_idx = 0

        while col_idx < num_columns:
            header = multi_headers[level][col_idx]
            span_count = 1
            row.append('')

            # Count consecutive identical headers for merging
            while (col_idx + span_count < num_columns and
                   multi_headers[level][col_idx + span_count] == header):
                span_count += 1
                row.append('')

            if level == 0 and header == '':
                row[col_idx] = ''
            else:
                if level == 0:
                    row[col_idx] = Paragraph(f"<b>{header}</b>", white_text_style)
                    style = white_text_style
                else:
                    row[col_idx] = Paragraph(f"<b>{header}</b>", custom_style)
                    style = custom_style

                # Background + text color (only for second level)
                if level != 0:
                    bg_color = "#d5dafb"
                    styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
                    styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.white))

                # Alignment and borders (both levels)
                styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
                styles.append(('LINEBELOW', (col_idx, level), (col_idx + span_count - 1, level), 1, colors.black))
                styles.append(('BOX', (col_idx, level), (col_idx + span_count - 1, level), 1, colors.black))

            if span_count > 1:
                styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            col_idx += span_count

        table_data.append(row)
        header_styles.extend(styles)

    # Fix vertical span for blank top-level headers
    for col_idx in range(num_columns):
        for level in range(num_levels - 1):
            if multi_headers[level][col_idx] == '' and multi_headers[level + 1][col_idx] != '':
                header_styles.append(('SPAN', (col_idx, level), (col_idx, num_levels - 1)))
                header_styles.append(('ALIGN', (col_idx, level), (col_idx, num_levels - 1), 'CENTER'))

    return table_data, header_styles
