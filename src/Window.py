# https://python-gtk-3-tutorial.readthedocs.io/en/latest/introduction.html
# To run: python3 Window.py

import gi
gi.require_version('Gtk', '3.0');
from gi.repository import Gtk

from huffman import Huffman;

class HuffmanWindow (Gtk.Window):

    def __init__ (self):
        Gtk.Window.__init__ (self, title= "Huffman Compressor");
        self.set_size_request (300, 180);

        main_box = Gtk.Box (orientation=Gtk.Orientation.HORIZONTAL, spacing=6);
        main_box.set_margin_left (6);
        main_box.set_margin_right (6);
        main_box.set_margin_top (6);
        main_box.set_margin_bottom (6);

        box = Gtk.Box (orientation=Gtk.Orientation.VERTICAL, spacing=6);
        box.set_hexpand (True);
        box.set_vexpand (True);

        self.separator = Gtk.Separator (orientation=Gtk.Orientation.VERTICAL);
        self.separator.set_visible (False);
        self.separator.set_no_show_all (True);

        main_box.add (box);
        main_box.add (self.separator);

        self.add (main_box);

        encode_label = Gtk.Label ("Encode text:");
        encode_label.set_halign (Gtk.Align.START);
        encode_label.get_style_context ().add_class ("h4");

        self.encode_entry = Gtk.Entry ();
        self.encode_entry.set_placeholder_text ("Text to compress...");
        self.encode_entry.connect ("changed", self.compress_text);

        self.file_chooser = Gtk.FileChooserButton (title="Text", action=Gtk.FileChooserAction.OPEN);
        self.file_chooser.connect ("file_set", self.file_set);

        file_label = Gtk.Label ("Input File:");
        file_label.set_halign (Gtk.Align.START);
        file_label.get_style_context ().add_class ("h4");

        box.add (encode_label);
        box.add (self.encode_entry);
        box.add (file_label);
        box.add (self.file_chooser);

        # Results UI
        self.results_revealer = Gtk.Revealer ();
        self.results_revealer.set_reveal_child (False);
        self.results_revealer.set_transition_type (Gtk.RevealerTransitionType.SLIDE_RIGHT);

        results_stack = Gtk.Stack ();
        results_stack.set_hhomogeneous (False);
        results_stack.set_vhomogeneous (False);

        switcher = Gtk.StackSwitcher ();
        switcher.set_stack (results_stack);
        switcher.set_halign (Gtk.Align.CENTER);

        scrollview = Gtk.ScrolledWindow ();
        scrollview.add (results_stack);
        scrollview.set_vexpand (True);
        scrollview.set_hexpand (True);

        results_box = Gtk.Box (orientation=Gtk.Orientation.VERTICAL, spacing=6);
        results_box.add (switcher);
        results_box.add (scrollview);

        self.results_revealer.add (results_box);
        main_box.add (self.results_revealer);

        # Frequency GUI
        self.frequency = Gtk.Label ("Character   Frequency    Code");
        self.frequency.set_use_markup (True);
        self.frequency.set_valign (Gtk.Align.START);
        results_stack.add_titled (self.frequency, "frequency", "Frequency");

        self.tree = Gtk.Label ("");
        results_stack.add_titled (self.tree, "tree", "Binary Tree");

        original_message = Gtk.Label ("Coded message:");
        original_message.set_halign (Gtk.Align.START);
        original_message.get_style_context ().add_class ("h4");

        compression_label = Gtk.Label ("New Size:");
        compression_label.set_halign (Gtk.Align.START);
        compression_label.get_style_context ().add_class ("h4");

        self.original_message = Gtk.Label ("");
        self.original_message.set_halign (Gtk.Align.START);
        self.original_message.get_style_context ().add_class ("dim-label");

        self.efficiency = Gtk.ProgressBar ();

        efficiency_box = Gtk.Box (orientation=Gtk.Orientation.VERTICAL, spacing=6);
        efficiency_box.add (original_message);
        efficiency_box.add (self.original_message);
        efficiency_box.add (self.original_message);
        efficiency_box.add (self.efficiency);

        results_stack.add_titled (efficiency_box, "efficiency", "Efficiency");

    # This is the text to compress. You get it after presing _enter_
    def compress_text (self, entry):
        huffman = Huffman ();
        huffman.originalMessage = str(entry.get_text ())
        huffman.startHuffmanCoding ();
        self.show_results (huffman);

    def file_set (self, file_chooser):
        openedFile = open (file_chooser.get_file ().get_path (), "r");
        text = ""
        for line in openedFile.readlines ():
            text += line

        huffman = Huffman ();
        huffman.originalMessage = text
        huffman.startHuffmanCoding ();
        self.show_results (huffman);

    def show_results (self, huffman):
        self.separator.set_visible (True);
        self.results_revealer.set_reveal_child (True);
        self.tree.set_label (self.format_tree (huffman));
        self.frequency.set_label (huffman.printFreqTable ());

        self.original_message.set_label (huffman.codedMessage);
        self.efficiency.set_fraction (huffman.efficiencyLevel);
        self.efficiency.set_text(str(huffman.efficiencyLevel) + '%')
        self.efficiency.set_show_text(True)



    def format_tree (self, huffman):
        lines = "{nodes}".format (nodes=huffman.node_list[0]).split ('(');
        result = '';

        indent_level = 0;
        for node in lines:
            node_str = "{node}\n".format (node=node);
            if node_str == "\n":
                continue;

            for x in range (0, indent_level):
                result = result + "    ";
            result = result + node_str.replace (")", "");

            closures = node_str.split (")");
            indent_level = indent_level + 2;
            for c in closures:
                indent_level = indent_level - 1;

        return result;

def main():
    win = HuffmanWindow ();
    win.connect ("delete-event", Gtk.main_quit);
    win.show_all ();
    Gtk.main ();

if __name__ == '__main__':
    main()
