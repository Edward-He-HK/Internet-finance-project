//
//  ContentView.swift
//  BeeCoin Wallet
//
//  Created by timlee on 6/11/2020.
//  Copyright © 2020 timlee. All rights reserved.
//

import SwiftUI

struct ContentView: View {
    @ObservedObject var viewModel = MainPageViewModel()
    var body: some View {
        //CryptoNetworkView()
        MainPageView(ViewModel: viewModel)
            
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
