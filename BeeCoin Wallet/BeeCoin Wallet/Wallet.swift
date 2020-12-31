//
//  Wallet.swift
//  BeeCoin Wallet
//
//  Created by timlee on 6/11/2020.
//  Copyright © 2020 timlee. All rights reserved.
//

import Foundation

class Wallet {

    var publicAddress: String = ""
    
    func getMyWalletAddress(){
        
        Network.getMyWalletAddress(node: "34.207.62.173:5000",  completionHandler: { status, address in if status {
            self.publicAddress = address ?? ""
            print(self.publicAddress)
            
            }
        })
    }
    
    var getPublicAddress: String {
        getMyWalletAddress()
        return self.publicAddress
    }
}
