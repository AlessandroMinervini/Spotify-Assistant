import sys
import os
import qdarkstyle
import cv2,numpy,face_recognition
from PyQt5.QtSql import *
from PyQt5.QtCore import Qt, QModelIndex,QSize
from PyQt5.QtWidgets import QWidget,QApplication, QVBoxLayout, QPushButton,QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QLineEdit, QLabel, QGridLayout

class Database_manage(QWidget):
    def __init__(self, parent=None):
        super(Database_manage, self).__init__(parent)
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(['ID', 'NOME' ,'TRACK','ARTIST', 'IMAGE_PATH'])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        self.lblName = QLabel("Nome:")
        self.txtName = QLineEdit()
        self.txtName.setPlaceholderText("Nome della persona")

        self.lblTrack = QLabel("Track:")
        self.txtTrack = QLineEdit()
        self.txtTrack.setPlaceholderText("Track preferita")

        self.lblArtist = QLabel("Artist:")
        self.txtArtist = QLineEdit()
        self.txtArtist.setPlaceholderText("Artista preferito")

        #self.lblID = QLabel("Image:")
        #self.botton_im = QPushButton('Mostra Database')
        #self.botton_im.clicked.connect(self.get_photo)

        grid = QGridLayout()
        grid.addWidget(self.lblName, 0, 0)
        grid.addWidget(self.txtName, 0, 1)
        grid.addWidget(self.lblTrack, 1, 0)
        grid.addWidget(self.txtTrack, 1, 1)
        grid.addWidget(self.lblArtist, 2, 0)
        grid.addWidget(self.txtArtist, 2, 1)

        btnCargar = QPushButton('Mostra Database')
        btnCargar.clicked.connect(self.look_data)

        btnInsertar = QPushButton('Inserisci Utente')
        btnInsertar.clicked.connect(self.insert_user)

        btnEliminar = QPushButton('Elimina Utente')
        btnEliminar.clicked.connect(self.delete_user)

        hbx = QHBoxLayout()
        hbx.addWidget(btnCargar)
        hbx.addWidget(btnInsertar)
        hbx.addWidget(btnEliminar)

        vbx = QVBoxLayout()
        vbx.addLayout(grid)
        vbx.addLayout(hbx)
        vbx.setAlignment(Qt.AlignTop)
        vbx.addWidget(self.table)

        self.setWindowTitle("Spotify Assistant")
        self.resize(400, 350)
        self.setLayout(vbx)

    def look_data(self, event):
        index = 0
        query = QSqlQuery()
        query.exec_("select * from person")

        while query.next():
            ids = query.value(0)
            nome = query.value(1)
            track = query.value(2)
            artist = query.value(3)
            path_image = query.value(4)

            self.table.setRowCount(index + 1)
            self.table.setItem(index, 0, QTableWidgetItem(str(ids)))
            self.table.setItem(index, 1, QTableWidgetItem(nome))
            self.table.setItem(index, 2, QTableWidgetItem(track))
            self.table.setItem(index, 3, QTableWidgetItem(artist))
            self.table.setItem(index, 4, QTableWidgetItem(path_image))

            index += 1
    def get_user(self,username):
        try:
            query = QSqlQuery()
            query.exec_('select * from person where firstname =' + Qt.__str__(username))
            while query.next():
                track = query.value(2)
                artist = query.value(3)
            return track,artist
        except:
            return '',''

    def insert_user(self,event):
        root, dirs, files = next(os.walk('spotyPeople'))
        ids = len(files)
        nome = self.txtName.text()
        track = self.txtTrack.text()
        artist = self.txtArtist.text()
        try:
            image_path = self.get_photo(nome)
        except:
            image_path = None
        query = QSqlQuery()
        #query.exec_("insert into person values(nome,track,artist,image_path)")
        query.exec_("insert into person values('{0}','{1}', '{2}','{3}','{4}')".format(ids,nome, track, artist, image_path))
        self.txtName.clear()
        self.txtTrack.clear()
        self.txtArtist.clear()

    def get_photo(self,nome):
        video_capture=cv2.VideoCapture(0)
        while True:
            ret, frame = video_capture.read()

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_frame = frame[:, :, ::-1]

            # Find all the faces and face enqcodings in the frame of video
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Loop through each face in this frame of video
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # See if the face is a match for the known face(s)
                name = "Unknown"
                # Draw a box around the face
                #cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                #font = cv2.FONT_HERSHEY_DUPLEX
                #cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)
            try:
                if cv2.waitKey(1) & 0xFF == ord('\r'):
                    face = frame[top - 60:bottom + 60, left - 60:right + 60]
                    cv2.imwrite(os.path.join("spotyPeople/" + nome + ".jpeg"), face)
                    break
            except:
                video_capture.release()
                cv2.destroyAllWindows()
            # Hit 'q' on the keyboard to quit!
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        return os.path.join("spotyPeople/"+nome+".jpeg")

    def delete_user(self, event):
        selected = self.table.currentIndex()
        if not selected.isValid() or len(self.table.selectedItems()) < 1:
            return

        ids = self.table.selectedItems()[0]
        query = QSqlQuery()
        query.exec_("select image_path from person where id = " + ids.text())
        while query.next():
            path=query.value(0)
        try:
            if (path != 'None'):
                os.remove(path)
        except:
            print('Lose Photo')

        query = QSqlQuery()
        query.exec_("delete from person where id = " + ids.text())

        self.table.removeRow(selected.row())
        self.table.setCurrentIndex(QModelIndex())

    def db_connect(self, filename, server):
        db = QSqlDatabase.addDatabase(server)
        db.setDatabaseName(filename)
        if not db.open():
            QMessageBox.critical(None, "Cannot open database",
                    "Unable to establish a database connection.\n"
                    "This example needs SQLite support. Please read the Qt SQL "
                    "driver documentation for information how to build it.\n\n"
                    "Click Cancel to exit.", QMessageBox.Cancel)
            return False
        return True

    def db_create(self):
        query = QSqlQuery()
        query.exec_("create table person(id INTEGER PRIMARY KEY NOT NULL UNIQUE , "
                    "firstname varchar(20), track varchar(20), artist varchar(20), image_path varchar(20))")
        #query.exec_("insert into person values(1,'wolmer','Ultimo','Next to me','')")
        #query.exec_("insert into person values(2,'alessandro','Artick Monkeys', '','')")

    def init(self, filename, server):
        import os
        if not os.path.exists(filename):
            self.db_connect(filename, server)
            self.db_create()
        else:
            self.db_connect(filename, server)

#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
#    ejm = Database_manage()
#    ejm.init('datafile', 'QSQLITE')
#    ejm.show()
#    sys.exit(app.exec_())
