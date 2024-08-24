from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

from jnius import autoclass

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
Environment = autoclass('android.os.Environment')
File = autoclass('java.io.File')
MediaStore = autoclass('android.provider.MediaStore')

class ImageSelectorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        self.image = Image()
        btn_select_image = Button(text='Select Image', on_press=self.select_image)
        
        layout.add_widget(btn_select_image)
        layout.add_widget(self.image)
        
        return layout

    def select_image(self, instance):
        intent = Intent()
        intent.setAction(Intent.ACTION_PICK)
        intent.setType("image/*")
        
        PythonActivity.mActivity.startActivityForResult(intent, 1)
        #PythonActivity.bind(onActivityResult=self.on_activity_result)
    
    def on_activity_result(self, requestCode, resultCode, data):
        if requestCode == 0 and resultCode == PythonActivity.RESULT_OK:
            selected_image_uri = data.getData()
            file_path = self.get_file_path_from_uri(selected_image_uri)
            self.image.source = file_path
    
    def get_file_path_from_uri(self, uri):
        cursor = PythonActivity.mActivity.getContentResolver().query(uri, None, None, None, None)
        cursor.moveToFirst()
        file_path_index = cursor.getColumnIndex(MediaStore.Images.ImageColumns.DATA)
        file_path = cursor.getString(file_path_index)
        cursor.close()
        
        return file_path

if __name__ == '__main__':
    ImageSelectorApp().run()