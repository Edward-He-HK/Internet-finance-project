//
//  paymentView.swift
//  BeeCoin Wallet
//
//  Created by timlee on 7/11/2020.
//  Copyright © 2020 timlee. All rights reserved.
//

import SwiftUI

struct paymentView: View {
    @State var payToAddress = ""
    @State var amount = ""
    @Binding var show : Bool
    @ObservedObject var ViewModel : MainPageViewModel
    @State var showPaymentSecurity = false
    let backgroundColor = Color(red: 40/255, green: 42/255, blue: 102/255)
    
    
    var body: some View {
        ZStack(){
            VStack(spacing : 12){
                    Spacer()
                    Text("Create Transaction")
                        .font(.system(size: 30))
                        .fontWeight(.bold)
                        //.foregroundColor()
                MultiLineTextField(text: $payToAddress)
                    Divider()
                    
                TextField("Amount: ", text: $amount).padding()
                Text("Expected Transaction Fee: \((Double(amount) ?? 0.0)*0.02)(2%)")
                    HStack{
                        
                        Spacer()
                        
                        Button(action: {
                            
                            self.showPaymentSecurity.toggle()
                            
                        }) {

                            Text("Confirm")
                        }.font(.headline)
                            .foregroundColor(.white)
                            .padding()
                            .frame(minWidth: 0, maxWidth: 100, minHeight: 0, maxHeight: 50)
                            .background(RoundedRectangle(cornerRadius: 8, style:   .circular).fill(Color.blue))
                            .padding(.bottom, 8)
                           
                        Spacer()
                        
                        Button(action: {
                            
                            self.show.toggle()
                        }) {
                            
                            Text("Cancel")
                        }.font(.headline)
                            .foregroundColor(.white)
                            .padding()
                            .frame(minWidth: 0, maxWidth: 100, minHeight: 0, maxHeight: 50)
                            .background(RoundedRectangle(cornerRadius: 8, style:   .circular).fill(Color.blue))
                            .padding(.bottom, 8)
                        
                    }.padding()
                    
                    
                }.padding()
            Spacer()
            if self.showPaymentSecurity{
                    
                    GeometryReader{_ in
                        
                        paymentSecurityView(show: self.$show, payToAddress: self.$payToAddress, amount: self.$amount ,ViewModel: self.ViewModel )
                        
                    }.background(
                        
                        Color.black.opacity(0.65)
                            .edgesIgnoringSafeArea(.all)
                            .onTapGesture {
                                withAnimation{
                                    self.showPaymentSecurity.toggle()
                                }
                            }
                    
                    )
                }
            
        }//.background(backgroundColor)
    }
}



