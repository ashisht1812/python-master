def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
    custom_style = self.get_custom_style()
    table_data = []
    header_styles = []

    num_levels = len(multi_headers)
    num_columns = len(multi_headers[-1])

    for level in range(num_levels):
        row = []
        styles = []
        col_idx = 0

        while col_idx < num_columns:
            header = multi_headers[level][col_idx]
            span_count = 1

            # Count consecutive identical headers for merging
            while (col_idx + span_count < num_columns and multi_headers[level][col_idx + span_count] == header):
                span_count += 1

            # If header is empty at the first level, add blank cell with no background
            if level == 0 and header == '':
                row.append('')
            else:
                row.append(Paragraph(f"<b>{header}</b>", custom_style))
                bg_color = "#1372be" if level == 0 else "#d5dafb"
                styles.append(('BACKGROUND', (col_idx, level), (col_idx + span_count - 1, level), colors.HexColor(bg_color)))
                styles.append(('TEXTCOLOR', (col_idx, level), (col_idx + span_count - 1, level), colors.white))

            if span_count > 1:
                styles.append(('SPAN', (col_idx, level), (col_idx + span_count - 1, level)))

            col_idx += span_count

        table_data.append(row)
        header_styles.extend(styles)

    return table_data, header_styles

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
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.HexColor("#d3d3d3")),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.HexColor("#d3d3d3")),
    ])

    # Remove the top and side borders for specific empty header columns
    for col_idx in no_top_border_columns:
        style.add('LINEABOVE', (col_idx, 0), (col_idx, 0), 0, colors.white)
        style.add('LINEBEFORE', (col_idx, 0), (col_idx, -1), 0, colors.white)
        style.add('BACKGROUND', (col_idx, 0), (col_idx, 0), colors.white)

    return style


base_style = self.create_table_style(style, no_top_border_columns=no_top_border_columns)
