def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers, no_top_border_columns=[]):
    from reportlab.lib import colors
    from reportlab.platypus import Paragraph
    from reportlab.lib.styles import ParagraphStyle

    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    # Define shared paragraph styles
    white_text_style = ParagraphStyle(
        name="WhiteHeaderStyle",
        parent=custom_style,
        textColor=colors.white,
        alignment=1,
    )

    black_text_style = ParagraphStyle(
        name="BlackHeaderStyle",
        parent=custom_style,
        textColor=colors.black,
        alignment=1,
    )

    for level in range(num_levels):
        row = []
        styles = []
        col_idx = 0

        while col_idx < num_columns:
            header = multi_headers[level][col_idx]
            span_count = 1
            row.append("")

            while (
                col_idx + span_count < num_columns and
                multi_headers[level][col_idx + span_count] == header
            ):
                span_count += 1
                row.append("")

            if level == 0 and header == "":
                row[col_idx] = ""
            else:
                style = white_text_style if level == 0 else black_text_style
                row[col_idx] = Paragraph(f"<b>{header}</b>", style)

                bg_color = "#1372be" if level == 0 else "#d5dafb"
                header_styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
                header_styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.white))
                header_styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))
                header_styles.append(('VALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'MIDDLE'))

            if span_count > 1:
                header_styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            col_idx += span_count

        table_data.append(row)
        header_styles.extend(styles)

    # Merge vertically those with empty top-level headers (like BM LT Vol, 1D Stdev)
    if num_levels == 2:
        for col_idx in range(num_columns):
            if multi_headers[0][col_idx] == '' and multi_headers[1][col_idx] != '':
                header_styles.append(('SPAN', (col_idx, 0), (col_idx, 1)))

    # Apply solid dark borders to the entire table area
    header_styles.append(('GRID', (0, 0), (-1, num_levels - 1), 1, colors.black))
    header_styles.append(('BOX', (0, 0), (-1, num_levels - 1), 1.5, colors.black))

    # If legacy config for top border removal is still passed
    for col_idx in no_top_border_columns:
        header_styles.append(('LINEABOVE', (col_idx, 0), (col_idx, 0), 0, colors.white))
        header_styles.append(('LINEBEFORE', (col_idx, 0), (col_idx, -1), 0, colors.white))
        header_styles.append(('LINEAFTER', (col_idx, 0), (col_idx, -1), 0, colors.white))
        header_styles.append(('BACKGROUND', (col_idx, 0), (col_idx, 0), colors.white))

    return table_data, header_styles
