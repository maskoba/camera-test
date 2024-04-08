import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.0
import QtQuick.Dialogs 1.2

ApplicationWindow {
    visible: true
    width: 640
    height: 520
    minimumWidth: width
    minimumHeight: height
    maximumWidth: width
    maximumHeight: height
    // x:1
    // y:0
    title: qsTr("Test")
    

    View1Form {
        id: page1
        button.onClicked: {
            backend.shot()
            // image.source = ""
            image.source = "image://myprovider/"+Math.random()
        }
    }
}
