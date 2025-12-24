def get_login_style ():
    
    return """
        QDialog { 
            background-color: #2c3e50; }
        QLabel { 
            color: white; font-size: 16px; }
        QLineEdit { 
            background-color: white; border-radius: 5px; padding: 8px; font-size: 14px; 
        }
                           
        #label {
            color: white;
            font-size: 24px;    
            font-weight: bold;
            qproperty-alignment: AlignCenter;           
        }
                           
        #label_10 {
            color: white;
            font-size: 13px;           
        }

        #btn_giris {
            background-color: #27ae60; color: white; border-radius: 8px; padding: 6px; font-weight: bold;
        }
        #btn_giris:hover { background-color: #2ecc71; }
        
        #btn_kayit {
            background-color: #2980b9; color: white; border-radius: 8px; padding: 6px; font-weight: bold;
        }
        #btn_kayit:hover { background-color: #3498db; }
    """

def get_main_style ():
    return """
        QMainWindow {
                background-color: #f0f2f5;
            }

            QLabel {
                color: #333333;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 14px;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                gridline-color: #eeeeee;
                color: #333333;
            }
            QHeaderView::section {
                background-color: #e1e4e8;
                padding: 6px;
                border: none;
                font-weight: bold;
                color: #333333;
            }

            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 6px;
                color: #333333;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #0078d7;
            }

            #lbl_toplam {
                font-size: 22px;
                font-weight: bold;
                color: #2e7d32;
                border: 2px solid #2e7d32;
                border-radius: 10px;
                padding: 10px;
                background-color: #e8f5e9;
            }

            #lbl_analiz_ciro {
                font-size: 22px;
                font-weight: bold;
                color: #2e7d32;
                border: 2px solid #2e7d32;
                border-radius: 10px;
                padding: 10px;
                background-color: #e8f5e9;
            }
            
            QGroupBox {
                border: 1px solid #dcdcdc;
                border-radius: 6px;
                margin-top: 10px;
                font-weight: bold;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }

            #tbl_takip {
                font-size: 16px;
            }
            
            #tbl_takip QHeaderView::section {
                font-size: 18px;
                height: 30px;
            }

            #tbl_depo {
                font-size: 16px;
            }
            
            #tbl_depo QHeaderView::section {
                font-size: 18px;
                height: 30px;
            }

            #tbl_analiz_detay QHeaderView::section {
                font-size: 16px;
                height: 30px;
            }

            
            QPushButton {
                background-color: #607d8b;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: normal;
                border: none;
            }

            #btn_onayla {
                background-color: #2e7d32;
                font-size: 20px;
                font-weight: bold;
                border-radius: 12px;
                padding: 15px;
            }
            #btn_onayla:hover { background-color: #0f5e13; }
            #btn_onayla:pressed { background-color: #043607; }


             #btn_stok_ekle {
                background-color: #2e7d32; /* Turuncu */
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
            }
            #btn_stok_ekle:hover { background-color: #0f5e13; }
            #btn_stok_ekle:pressed { background-color: #043607; }

            #btn_analiz_yenile {
                background-color: #2e7d32;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                border-radius: 6px;
            }
            #btn_analiz_yenile:hover { background-color: #0f5e13; }
            #btn_analiz_yenile:pressed { background-color: #043607; }

            #btn_teslim_et {
                background-color: #d32f2f;
                font-size: 20px;
                font-weight: bold;
                padding: 12px;
                border-radius: 10px;
            }
            #btn_teslim_et:hover { background-color: #b71c1c; }
            #btn_teslim_et:pressed { background-color: #750b0b; }

            #btn_depo_yenile {
                background-color: #e1e4e8;
                color: #333333;
                font-size: 16px;
                font-weight: bold;
                padding: 8px;
                border-radius: 10px;
            }
            #btn_depo_yenile:hover { background-color: #abadb0; }
            #btn_depo_yenile:pressed { background-color: #7d7e80; }

        """

def get_menu_btn_style():
    return """
            QPushButton {
                background-color: #607d8b;
                color: white;
                font-weight: bold;
                font-size: 10pt;
                border-radius: 6px;
                border: none;
                padding: 5px;
                margin: 1px;
            }
            QPushButton:hover {
                background-color: #455a64;
            }
            QPushButton:pressed {
                background-color: #263238;
            }

    """
