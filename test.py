from wonderguy import Display, wb_tool, Control
# wb_tool.show_console()

d = Display()
c = Control()

for i in range(5):
    d.print(1,1,i)
    v = c.get_sw4()
    print(v)