//
//  MultiLineTextField.swift
//  FocusBeetle
//
//  Created by timlee on 30/10/2020.
//  Copyright © 2020 timlee. All rights reserved.
//

import Foundation
import SwiftUI
import UIKit

struct MultiLineTextField: UIViewRepresentable {


func makeCoordinator() -> Coordinator {
    
    return MultiLineTextField.Coordinator(parent1: self)
}

@Binding var text : String

func makeUIView(context: Context) -> UITextView {
    
    let view = UITextView()
    view.text = "Pay to:"
    view.textColor = .black
    view.font = .systemFont(ofSize: 18)
    view.backgroundColor = .clear
    view.returnKeyType = .done
    view.delegate = context.coordinator
    return view
}

func updateUIView(_ uiView: UITextView, context: Context) {
    
}

class Coordinator : NSObject,UITextViewDelegate{
    
    var parent : MultiLineTextField
    
    init(parent1 : MultiLineTextField) {
        
        parent = parent1
    }
    
    func textViewDidChange(_ textView: UITextView) {
        
        parent.text = textView.text
    }
    
    func textViewDidEndEditing(_ textView: UITextView) {
     
        if parent.text == ""{
            
            parent.text = "About You !!!"
        }
    }
    
    func textViewDidBeginEditing(_ textView: UITextView) {
        
        if parent.text == ""{
            
            textView.text = ""
        }
    }
}
}
