def create_table_style(self, style_config, no_top_border_columns=[]):
    style = TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#000000")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('INNERGRID', (0, 0), (-1, -1), 0.1, colors.HexColor("#d3d3d3")),
        ('BOX', (0, 0), (-1, -1), 0.1, colors.HexColor("#d3d3d3")),
    ])

    # Remove vertical borders for first header row
    first_level_headers = style_config.get('first_level_header_spans', [])
    col_idx = 0
    for span in first_level_headers:
        span_count = span['span_count']
        if span['header'] == "":
            # Remove top border and background for empty headers
            style.add('LINEABOVE', (col_idx, 0), (col_idx + span_count - 1, 0), 0, colors.white)
            style.add('BACKGROUND', (col_idx, 0), (col_idx + span_count - 1, 0), colors.white)
        else:
            # Remove vertical borders within the span for non-empty headers
            for inner_col in range(col_idx + 1, col_idx + span_count):
                style.add('LINEBEFORE', (inner_col, 0), (inner_col, 0), 0, colors.white)
        col_idx += span_count

    # Remove top borders for specified columns
    for col_idx in no_top_border_columns:
        style.add('LINEABOVE', (col_idx, 0), (col_idx, 0), 0, colors.white)
        style.add('BOX', (col_idx, 0), (col_idx, 0), 0, colors.white)

    return style
def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    empty_column = 0
    for col in multi_headers[0]:
        if col == "":
            empty_column += 1
        else:
            break

    # Keep track of spans for first-level headers
    first_level_header_spans = []
    col_idx = 0
    headers = multi_headers[0]
    while col_idx < num_columns:
        header = headers[col_idx]
        span_count = 1
        while col_idx + span_count < num_columns and headers[col_idx + span_count] == header:
            span_count += 1
        first_level_header_spans.append({'header': header, 'span_count': span_count})
        col_idx += span_count

    # Store span information for style adjustments
    style_config = {
        'first_level_header_spans': first_level_header_spans
    }

    # Construct header rows
    for level in range(num_levels):
        headers = multi_headers[level]
        row = []
        styles = []
        col_idx = 0
        while col_idx < num_columns:
            header = headers[col_idx]
            span_count = 1
            while col_idx + span_count < num_columns and headers[col_idx + span_count] == header:
                span_count += 1
            while len(row) <= col_idx:
                row.append("")

            row[col_idx] = Paragraph(f"<b>{header}</b>", custom_style)

            # Apply background color based on header level
            bg_color = "#d5dafb" if level == 1 else "#1372be"
            text_color = colors.white if level == 0 else colors.black

            styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))
            styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
            styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), text_color))
            styles.append(('ALIGN', (col_idx, level), (col_idx + span_count - 1, level), 'CENTER'))

            col_idx += span_count

        table_data.append(row)
        header_styles.extend(styles)

    # Construct data rows
    for _, row in dataframe.iterrows():
        data_row = [Paragraph(str(row[col_info['column']]), custom_style) for col_info in report_column_info]
        table_data.append(data_row)

    return table_data, header_styles, style_config
def create_table(self, data, style, relative_width, multi_level_headers, additional_styles=None, style_config=None):
    max_width = landscape(letter)
    total_width = max_width[0]
    column_widths = self.calculate_width(relative_width, total_width)

    repeat_rows = len(multi_level_headers)

    table = Table(data, colWidths=column_widths, repeatRows=repeat_rows, splitByRow=True)

    base_style = self.create_table_style(style_config)

    if additional_styles:
        combined_styles = base_style.getCommands() + additional_styles
        table.setStyle(TableStyle(combined_styles))
    else:
        table.setStyle(base_style)

    return table

multi_level_headers:
  - ['', '', '', '', '6M Avg', '6M Avg', '6M Avg', '6M Avg', '', '', '', '', '', '']
  - ['Team', 'Subteam', 'Fund', 'Benchmark', 'MV (MM)', 'LB', 'UB', 'Prev', 'Avg', 'Curr', 'Prev', 'Curr', 'BM', 'Port', 'BM', 'BM LT Vol', '1D Std ev']
