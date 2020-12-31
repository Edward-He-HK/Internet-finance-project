//
//  MainPageViewModel.swift
//  BeeCoin Wallet
//
//  Created by timlee on 6/11/2020.
//  Copyright © 2020 timlee. All rights reserved.
//

import Foundation
import SwiftUI
import CoreData
import UIKit


class MainPageViewModel : ObservableObject{
    var timer = Timer()
    let wallet = Wallet()
    let network = Network()
    @State var show = false
    @Published var myBalance: String
    @Published var myWalletAddress: String
    
    init() {
        myBalance = "Loading"
        myWalletAddress = "Loading"
        myWalletAddress = wallet.getPublicAddress
        self.updateBalance()
        timer = Timer.scheduledTimer(timeInterval: 1, target: self, selector: #selector(self.updateData), userInfo: nil, repeats: true)
        
    }
    
    @objc func updateData() {
        updateBalance()
    }
    
    func getAddress(){
        myWalletAddress = wallet.getPublicAddress
    }
    
    func updateBalance(){
        getAddress()
        Network.checkMyBalance(node: "34.207.62.173:5000", address:  self.myWalletAddress,
                           completionHandler: { status, balance in if status {
                print(balance as Any)
                self.myBalance = balance ?? "0.0"
                            print(self.myBalance)
            }
        })
    }
    
    func mining(){
        Network.mine(node: "34.207.62.173:5000", address:  self.myWalletAddress, completionHandler: { status, record in if status {
                        
                        print(self.myBalance)
            }})
    }
    
    
    func makeTransaction(recipient: String, amount: String){

        Network.makeNewTransaction(node: "34.207.62.173:5000", recipient_address: recipient, amount: amount, completionHandler: { status, result in
            if status {

            }
        })

    }
   
    
    
    @objc private func updateInterest() {
        // how long we've been running in the current .running state
        // and add in any previously accumulated time
        
        Network.getInterest(node: "34.207.62.173:5000", address:  self.myWalletAddress, completionHandler: { status, interst in if status {
                    
                    print ("interest")
        }})
    }
}
