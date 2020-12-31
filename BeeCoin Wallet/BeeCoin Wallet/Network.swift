//
//  Network.swift
//  BeeCoin Wallet
//
//  Created by timlee on 6/11/2020.
//  Copyright © 2020 timlee. All rights reserved.
//

import Foundation
import Alamofire

class Network {

    static func checkMyBalance(node: String, address: String, completionHandler: @escaping (Bool, String?) -> ()) {
        let parameter = ["address": address]
        AF.request("http://" + node + "/check_my_balance", method: .post, parameters: parameter)
            .responseString { response in
                switch (response.result) {
                case .success(let result):
                    completionHandler(true, result)
                case .failure:
                    completionHandler(false, nil)
                }
        }
    }
    static func makeNewTransaction(node: String, recipient_address: String, amount:String, completionHandler: @escaping (Bool, String?) -> ()) {
           let parameter = [
               "recipient_address": recipient_address,
               "amount": amount,
           ]
           AF.request("http://" + node + "/new_transaction", method: .post, parameters: parameter)
               .responseString { response in
                   switch (response.result) {
                   case .success(let result):
                       completionHandler(true, result)
                   case .failure:
                       completionHandler(false, nil)
                   }
                   
           }
           
    }

    static func mine(node: String, address: String, completionHandler: @escaping (Bool, String?) -> ()) {
        let parameter = ["address": address]
        AF.request("http://" + node + "/mine", method: .get, parameters: parameter)
            .responseString { response in
                switch (response.result) {
                case .success(let result):
                    completionHandler(true, result)
                case .failure:
                    completionHandler(false, nil)
                }
        }
    }
    
    static func getMyWalletAddress(node: String, completionHandler: @escaping (Bool, String?) -> ()) {
        AF.request("http://" + node + "/return_address", method: .post)
            .responseString { response in
                switch (response.result) {
                case .success(let result):
                    completionHandler(true, result)
                case .failure:
                    completionHandler(false, nil)
                }
        }
    }
    
    static func getInterest(node: String, address: String, completionHandler: @escaping (Bool, String?) -> ()) {
        let parameter = ["address": address]
        AF.request("http://" + node + "/interest2", method: .post, parameters: parameter)
            .responseString { response in
                switch (response.result) {
                case .success(let result):
                    completionHandler(true, result)
                case .failure:
                    completionHandler(false, nil)
                }
        }
    }
}

