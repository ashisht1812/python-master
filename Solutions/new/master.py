from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class ReportEngine:
    def get_custom_style(self):
        styles = getSampleStyleSheet()
        s = styles['BodyText']
        s.wordWrap = 'CJK'
        s.fontName = 'Helvetica'
        s.fontSize = 7
        s.leading = 10
        return s

    def calculate_width(self, relative_width, total_width):
        """Turn [2,3,1] + 600pt → [150,225,75]"""
        total = sum(relative_width)
        return [(w/total)*total_width for w in relative_width]

    def prepare_table_data(self, report_column_info, df, group_colors, multi_headers):
        """
        Returns (data, header_styles)
        - data: list of rows, each row is a list of Paragraphs or ""
        - header_styles: list of TableStyle commands to apply spans, backgrounds, etc.
        """
        custom_style = self.get_custom_style()
        n_levels = len(multi_headers)
        n_cols   = len(multi_headers[-1])

        # count how many leading empty cols in level 0
        empty_cols = 0
        for h in multi_headers[0]:
            if h == "":
                empty_cols += 1
            else:
                break

        data = []
        header_styles = []

        # -- build header rows --
        for level in range(n_levels):
            row = [""]*n_cols
            col = 0
            while col < n_cols:
                text = multi_headers[level][col]
                # count span
                span = 1
                while col+span < n_cols and multi_headers[level][col+span] == text:
                    span += 1

                if text:
                    # insert Paragraph
                    row[col] = Paragraph(f"<b>{text}</b>", custom_style)

                    # background/color differs by level
                    bg = "#D5DAFB" if level==0 else "#EEF3FB"
                    header_styles.append(('BACKGROUND',(col,level),(col+span-1,level),colors.HexColor(bg)))
                    header_styles.append(('TEXTCOLOR',(col,level),(col+span-1,level),colors.black))
                    header_styles.append(('SPAN',(col,level),(col+span-1,level)))

                # optionally remove top border on blank first-level cols
                # (we’ll do that in create_table_style via no_top_border_columns)

                col += span

            data.append(row)

        # -- build body rows --
        # your existing code to group, aggregate, iterate df → body_rows
        # here we just sketch:
        for _, dr in df.iterrows():
            row = []
            for col_info in report_column_info:
                val = dr[col_info['column']]
                row.append(Paragraph(str(val), custom_style))
            data.append(row)

        return data, header_styles

    def create_table_style(self, style_config, no_top_border_columns=[]):
        """
        style_config: your base style (we ignore here and hard-code)
        no_top_border_columns: list of ints where we erase the top grid line
        """
        cmds = [
            # base font/color/grid
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TEXTCOLOR',(0,0),(-1,0),colors.black),
            ('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),
            ('FONTSIZE',(0,0),(-1,0),8),
            ('LINEBELOW',(0,0),(-1,0),0.5,colors.black),
            ('INNERGRID',(0,0),(-1,-1),0.25,colors.HexColor("#d3d3d3")),
            ('BOX',(0,0),(-1,-1),0.5,colors.HexColor("#d3d3d3")),
        ]

        # remove top border for blank header cols
        for c in no_top_border_columns:
            cmds.append(('LINEABOVE',(c,0),(c,0),0,colors.white))
            cmds.append(('BOX',(c,0),(c,0),0,colors.white))

        return TableStyle(cmds)

    def create_table(self, report_column_info, df, group_colors,
                     relative_width, multi_headers, no_top_border_columns=[]):
        # 1) build data + per-cell header styles
        data, header_styles = self.prepare_table_data(
            report_column_info, df, group_colors, multi_headers
        )

        # 2) compute column widths
        page_w, _ = landscape(letter)
        widths = self.calculate_width(relative_width, page_w)

        # 3) build the Table
        table = Table(data, colWidths=widths,
                      repeatRows=len(multi_headers), splitByRow=True)

        # 4) apply the combined styles
        base = self.create_table_style(None, no_top_border_columns)
        combined = base.getCommands() + header_styles
        table.setStyle(TableStyle(combined))

        return table
