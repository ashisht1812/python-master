from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors

class ReportEngine:
    # … all your other methods …

    def calculate_width(self, relative_width, total_width):
        """
        Given a list of relative widths and the total available width,
        return a list of absolute column widths.
        """
        total_rel = sum(relative_width)
        return [(w / total_rel) * total_width for w in relative_width]

    def create_table(self,
                     data,
                     style_config,              # list of TableStyle rules from your YAML (or None)
                     relative_width,            # [ w1, w2, … ]
                     multi_level_headers,       # [ ["", "", …], ["Team","Subteam",…] ]
                     no_top_border_columns=None # [0,1,2]  — these first‐level header cols get no top border
                     ):
        # 1) compute widths & header repetition
        max_w      = landscape(letter)[0]
        col_widths = self.calculate_width(relative_width, max_w)
        repeat     = len(multi_level_headers)

        # 2) build the Table
        tbl = Table(
            data,
            colWidths=col_widths,
            repeatRows=repeat,
            splitByRow=True
        )

        # 3) apply **all** styling in one place
        tbl.setStyle(
            self.create_table_style(style_config, no_top_border_columns or [])
        )
        return tbl

    def create_table_style(self,
                           style_config,              # your per-column overrides from YAML
                           no_top_border_columns=None # [0,1,2]
                           ):
        """
        Returns a ReportLab TableStyle that:
         • sets textcolor, padding, grid, etc.
         • removes the top border on the specified first-level header cols
         • finally appends any extra rules from style_config
        """
        no_tb = no_top_border_columns or []

        cmd = TableStyle([
            # base text & header underline
            ('TEXTCOLOR',   (0,0), (-1,0), colors.black),
            ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',      (0,0), (-1,-1), 'TOP'),
            ('LINEBELOW',   (0,0), (-1,0), 0.5, colors.black),

            # consistent padding
            ('LEFTPADDING',  (0,0), (-1,-1), 3),
            ('RIGHTPADDING', (0,0), (-1,-1), 3),
            ('TOPPADDING',   (0,0), (-1,-1), 3),
            ('BOTTOMPADDING',(0,0), (-1,-1), 3),

            # grid & outer box
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.HexColor('#d3d3d3')),
            ('BOX',       (0,0), (-1,-1), 0.1,  colors.HexColor('#d3d3d3')),
        ])

        # remove top border on selected columns
        for col in no_tb:
            # wipe out the top line on that single cell
            cmd.add('LINEABOVE', (col,0), (col,0), 0, colors.white)
            # also clear any little BOX corner stroke
            cmd.add('BOX',       (col,0), (col,0), 0, colors.white)

        # finally append any extra rules from your YAML config
        if style_config:
            for rule in style_config:
                cmd.add(*rule)

        return cmd

    # … your other methods …



    # pull out the two pieces
    style_cfg = table_config.get('table_style', None)
    no_tb     = table_config.get('no_top_border_columns', [])

    # create_table now does *all* the styling internally
    table = self.create_table(
        table_data,
        style_cfg,
        relative_width,
        multi_level_headers,
        no_top_border_columns=no_tb
    )
    elements.append(table)
