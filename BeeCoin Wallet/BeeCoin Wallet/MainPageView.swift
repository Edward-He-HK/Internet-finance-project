//
//  MainPageView.swift
//  BeeCoin Wallet
//
//  Created by timlee on 6/11/2020.
//  Copyright © 2020 timlee. All rights reserved.
//

import SwiftUI

struct MainPageView : View {
    @ObservedObject var ViewModel : MainPageViewModel
    @State var show = false
    
    var body : some View{
        
        ZStack{
            
            VStack(spacing: 10){
                HStack(spacing: 15){
                    
                    Image("BeeCoin").resizable().frame(width:70, height: 70).clipped()
                    
                    Text("BeeCoin Wallet").font(.title)
                    
                    Spacer()
                    
                    Button(action: {
                        
                    }) {
                        
                        Image("menu").renderingMode(.original)
                    }
                }
                .edgesIgnoringSafeArea(.top)
                .background(Color.orange.opacity(0.7))
                .cornerRadius(20)
                
                HStack{
                    
                    Text("Account Overview")
                    
                    Spacer()
                    
                    Button(action: {
                        self.ViewModel.updateBalance()
                    }) {
                        Image("refresh").renderingMode(.original).resizable().frame(width:30, height: 30).clipped()
                    }
                    
                }.padding(.top,5)
                
                HStack{
                    
                    VStack(alignment: .leading, spacing: 10) {
                        
                        Text("Current Balance: \(ViewModel.myBalance)")
                        Button(action: {
                            UIPasteboard.general.string = self.ViewModel.myWalletAddress
                        }) {
                            Text("Wallet Address: ")
                             Spacer()
                            Image(systemName: "square.and.pencil").renderingMode(.original)
                        }
                        Text(ViewModel.myWalletAddress)
                       
                    }

                }
                .padding(20)
                .background(Color.gray.opacity(0.2))
                .cornerRadius(20)
                .padding(.top)
                
                Spacer()
                
                HStack{
                
                    Group{
                        Button(action: {
                            self.ViewModel.mining()
                        }) {
                            Image("golden-fever").renderingMode(.original).resizable().frame(width:30, height: 30).clipped()
                            Text("Mine ")
                            
                            
                        }
                        //.background(Color.gray.opacity(0.3))
                        .cornerRadius(20)
                        .padding()

                        Button(action: {
                            self.show.toggle()
                        }) {
                            Image("payment").renderingMode(.original).resizable().frame(width:30, height: 30).clipped()
                            Text("Transaction ").foregroundColor(Color.blue)
                        }
                        
                    }.padding(.top)
                    .sheet(isPresented: $show) {
                        paymentView(show: self.$show, ViewModel: self.ViewModel)
                    }
                
                }
                .padding(.vertical,8)
                .padding(.bottom)
                .animation(.default)
                
            }.padding([.horizontal,.top])
            
        }.animation(.default)
    }
}



//struct MainPageView_Previews: PreviewProvider {
//    static var previews: some View {
//        MainPageView()
//    }
//}
