# https://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html
# To run: python3 Window.py

import gi
gi.require_version('Gtk', '3.0');
from gi.repository import Gtk

from huffman import Huffman;

class HuffmanWindow (Gtk.Window):

    def __init__ (self):
        Gtk.Window.__init__ (self, title= "Huffman Compressor");
        self.set_size_request (200, 100);

        box = Gtk.Box (orientation=Gtk.Orientation.VERTICAL, spacing=6);
        box.set_margin_left (6);
        box.set_margin_right (6);
        box.set_margin_top (6);
        box.set_margin_bottom (6);

        self.add (box)

        encode_label = Gtk.Label ("Encode text:");
        encode_label.set_halign (Gtk.Align.START);
        encode_label.get_style_context ().add_class ("h4");

        self.encode_entry = Gtk.Entry ();
        self.encode_entry.set_placeholder_text ("Text to compress...");
        self.encode_entry.connect ("activate", self.compress_text);

        self.file_chooser = Gtk.FileChooserButton (title="Text", action=Gtk.FileChooserAction.OPEN);
        self.file_chooser.connect ("file_set", self.file_set);

        file_label = Gtk.Label ("Input File:");
        file_label.set_halign (Gtk.Align.START);
        file_label.get_style_context ().add_class ("h4");

        box.add (encode_label);
        box.add (self.encode_entry);
        box.add (file_label);
        box.add (self.file_chooser);

    # This is the text to compress. You get it after presing _enter_
    def compress_text (self, entry):
        huffman = Huffman ();
        huffman.originalMessage = str(entry.get_text ())
        huffman.startHuffmanCoding ();

    def file_set (self, file_chooser):
        openedFile = open (file_chooser.get_file ().get_path (), "r");
        text = ""
        for line in openedFile.readlines ():
            text += line

        huffman = Huffman ();
        huffman.originalMessage = text
        huffman.startHuffmanCoding ();

def main():
    win = HuffmanWindow ();
    win.connect ("delete-event", Gtk.main_quit);
    win.show_all ();
    Gtk.main ();

if __name__ == '__main__':
    main()
