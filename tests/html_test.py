# -*- coding: utf-8 -*-
import MarkupPy

title = "Useless Inc."
header = "Some information at the top, perhaps a menu."
footer = "This is the end."
styles = ( 'layout.css', 'alt.css', 'images.css' )

page = MarkupPy.page( )
page.init( css=styles, title=title, header=header, footer=footer )
page.br( )
    
paragraphs = ( "This will be a paragraph.",
              "So as this, only slightly longer, but not much.",
              "Third absolutely boring paragraph." )

page.p( paragraphs )
        
page.a( "Click this.", class_='internal', href='index.html' )
page.img( width=60, height=80, alt='Fantastic!', src='fantastic.jpg' )
print(page)
            