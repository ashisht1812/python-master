from reportlab.lib import colors
from reportlab.platypus import TableStyle, Paragraph

class ReportEngine:
    # … your other methods …

    def prepare_table_data(self, report_column_info, dataframe, group_colors, multi_headers):
        custom_style = self.get_custom_style()
        table_data = []
        header_styles = []

        num_levels  = len(multi_headers)
        num_columns = len(multi_headers[-1])

        # count how many empty slots at the left of level-0
        empty_slots = 0
        for h in multi_headers[0]:
            if h == "":
                empty_slots += 1
            else:
                break

        # build each header level
        for level, headers in enumerate(multi_headers):
            row   = [""] * num_columns
            styles = []

            col_idx = 0
            while col_idx < num_columns:
                header    = headers[col_idx]
                # figure out how many subsequent slots are identical
                span      = 1
                while (col_idx + span < num_columns
                       and headers[col_idx+span] == header):
                    span += 1

                # only paint non-empty first–level headers
                if level == 0 and header:
                    styles.append((
                        'BACKGROUND',
                        (col_idx, level),
                        (col_idx + span - 1, level),
                        colors.HexColor("#c5cbea")   # your lilac
                    ))
                    styles.append((
                        'TEXTCOLOR',
                        (col_idx, level),
                        (col_idx + span - 1, level),
                        colors.black
                    ))
                # paint second–level headers
                elif level == 1:
                    styles.append((
                        'BACKGROUND',
                        (col_idx, level),
                        (col_idx + span - 1, level),
                        colors.HexColor("#e5eefa")  # light-grey
                    ))

                # put the text in
                if header:
                    row[col_idx] = Paragraph(f"<b>{header}</b>", custom_style)

                # draw inner grid lines only for true header rows
                styles.append(('GRID',
                               (col_idx, level),
                               (col_idx + span - 1, level),
                               0.25, colors.HexColor("#d3d3d3")))
                # center align
                styles.append(('ALIGN',
                               (col_idx, level),
                               (col_idx + span - 1, level),
                               'CENTER'))

                col_idx += span

            table_data.append(row)
            header_styles.extend(styles)

        return table_data, header_styles


    def create_table(self, data, style, relative_width, multi_level_headers, no_top_border_columns=None):
        # build the table
        table = Table(
            data,
            colWidths=self.calculate_width(relative_width),
            repeatRows=len(multi_level_headers),
            splitByRow=True
        )

        # base style
        base = self.create_table_style(style, no_top_border_columns or [])
        table.setStyle(base)

        return table


    def create_table_style(self, style_config, no_top_border_columns):
        """
        style_config: your config object (unused here since we hardcode)
        no_top_border_columns: list of integer column‐indices to lift the
                               top border on (for fully blank first headers).
        """
        s = TableStyle([
            # default text, alignment, box
            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
            ('ALIGN',     (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',    (0,0), (-1,-1), 'TOP'),
            ('FONTNAME',  (0,0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE',  (0,0), (-1, 0), 8),
            ('LINEBELOW', (0,0), (-1, 1), 0.5, colors.black),

            # full grid for all cells
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor("#d3d3d3")),
            ('BOX',       (0,0), (-1,-1), 0.25, colors.HexColor("#d3d3d3")),
        ])

        # lift the top border (and left/right) for blank header cols
        for col in no_top_border_columns:
            s.add('LINEABOVE', (col,0), (col,0), 0, colors.white)
            s.add('BOX',       (col,0), (col,0), 0, colors.white)

        return s
