import QtQuick 2.11
import QtQuick.Window 2.11
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.0
import QtQuick.Dialogs 1.2

Item {
    id: page1
    width: 640
    height: 520
    property alias image: image
    property alias button: button

    Button {
        id: button
        x: 0
        y: 480
        width: 640
        height: 40
        text: qsTr("Shutter")
    }

    Image {
        id: image
        x: 0
        y: 0
        width: 640
        height: 480
        source: "image://myprovider/test"
        sourceSize.height: 300
        sourceSize.width: 400
        fillMode: Image.PreserveAspectFit
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/

