//
//  paymentSecurityView.swift
//  BeeCoin Wallet
//
//  Created by timlee on 7/11/2020.
//  Copyright © 2020 timlee. All rights reserved.
//

import SwiftUI

struct paymentSecurityView: View {
       @State private var password = ""
       @State private var correctPassword = "123456"
       @State private var showPassword = false
       @Binding var show : Bool
       @Binding var payToAddress : String
       @Binding var amount : String
       @State var showsAlert = false
       @State var validePassword = false
       @State var valideAmount = false
       @ObservedObject var ViewModel : MainPageViewModel
    
        let backgroundColor = Color(red: 40/255, green: 42/255, blue: 102/255)
       var body: some View {
           ZStack {
            
               VStack {
                   
                   HStack {
                       Image(systemName: "lock")
                           .foregroundColor(.secondary)
                       if showPassword {
                           TextField("Password",
                           text: $password)
                       } else {
                       SecureField("Password",
                                 text: $password)
                       }
                       Button(action: { self.showPassword.toggle()}) {

                           Image(systemName: "eye")
                           .foregroundColor(.secondary)
                       }
                   }.padding()
                    .background(Capsule().fill(Color.gray.opacity(0.3)))
                
                    Button(action: {
                        
                        if(self.correctPassword==self.password){
                        //Enter Correct Password

                            if( self.ViewModel.myBalance >= self.amount){
                                self.ViewModel.makeTransaction(recipient: self.payToAddress, amount: self.amount)
                                self.valideAmount = true
                                
                            }
                            else{
                                self.valideAmount = false
                            }
                            
                            self.validePassword = true
                            
                        }
                        self.showsAlert = true

                        
                    }) {

                            Text("confirm")
                    }.alert(isPresented: self.$showsAlert){
                        
                        Alert(title: Text(self.validePassword && self.valideAmount ? "Transaction Success":"Transaction Fail"), message: Text(self.validePassword ? (self.valideAmount ? "Wait for a second for mining" : "The amount must not larger than the coins you owned !"): "Incorrect Password"), dismissButton: .default(Text("Ok"), action: {if(self.validePassword){
                            
                                
                                self.show.toggle()
                            
                            }}))
                        
                    }
                    .font(.headline)
                    .foregroundColor(.white)
                    .padding()
                    .frame(minWidth: 0, maxWidth: 100, minHeight: 0, maxHeight: 50)
                    .background(RoundedRectangle(cornerRadius: 8, style:   .circular).fill(Color.blue))
                    .padding(.bottom, 8)
                
                }.padding()
           }.padding()
           .background(Color.white)
           .cornerRadius(10)
       }
}



//struct paymentSecurityView_Previews: PreviewProvider {
//    static var previews: some View {
//        paymentSecurityView()
//    }
//}
