import gui_components.gui_main
import db_components.db_control

if __name__ == '__main__':
 db = db_components.db_control.BancoDados()
 db.monta_tabelas()

 app = gui_components.gui_main.MainWindow()
 app.mainloop()

