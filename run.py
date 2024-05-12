import sys

import nn_sim.ui.helpers.uihelper as dc
import nn_sim.ui.resources.resources_fonts
import nn_sim.ui.resources.resources_material_icons
from nn_sim.ui.windows import MainWindow

import qtmodern.styles

ctx = dc.ApplicationContext()
app = dc.Application(ctx, sys.argv)
qtmodern.styles.dark(app)
dc.app_set_font(app, font_size=16)


mw = MainWindow(ctx)
mw.show()

sys.exit(app.exec())
