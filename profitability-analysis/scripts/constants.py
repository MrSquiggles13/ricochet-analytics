REX_MARKETS = {
    "DaiToWeth": "0x9BEf427fa1fF5269b824eeD9415F7622b81244f5",
    "WethToDai": "0x0A70Fbb45bc8c70fb94d8678b92686Bb69dEA3c3",
    "UsdcToWbtc": "0xe0A0ec8dee2f73943A6b731a2e11484916f45D44",
    "WbtcToUsdc": "0x71f649EB05AA48cF8d92328D1C486B7d9fDbfF6b",
    "UsdcToWeth": "0x8082Ab2f4E220dAd92689F3682F3e7a42b206B42",
    "WethToUsdc": "0x3941e2E89f7047E0AC7B9CcE18fBe90927a32100",
    "UsdcToMatic": "0xE093D8A4269CE5C91cD9389A0646bAdAB2c8D9A3",
    "MaticToUsdc": "0x93D2d0812C9856141B080e9Ef6E97c7A7b342d7F",
    "DaiToMatic": "0xA152715dF800dB5926598917A6eF3702308bcB7e",
    "MaticToDai": "0x250efbB94De68dD165bD6c98e804E08153Eb91c6",
    "UsdcToMkr": "0xC89583Fa7B84d81FE54c1339ce3fEb10De8B4C96",
    "MkrToUsdc": "0xdc19ed26aD3a544e729B72B50b518a231cBAD9Ab",
    "DaiToMkr": "0x47de4Fd666373Ca4A793e2E0e7F995Ea7D3c9A29",
    "MkrToDai": "0x94e5b18309066dd1E5aE97628afC9d4d7EB58161",
    "UsdcToIdle": "0xBe79a6fd39a8E8b0ff7E1af1Ea6E264699680584",
    "UsdcToRexslpEthUsdc": "0xeb367F6a0DDd531666D778BC096d212a235a6f78",
    "UsdcToRexslpEthIdle": "0x0cb9cd99dbC614d9a0B31c9014185DfbBe392eb5",
    "UsdcToRic": "0x98d463A3F29F259E67176482eB15107F364c7E18"
}

REX_MARKET_BLOCK_START = {
    "DaiToWeth": 19387075,
    "WethToDai": 19391568,
    "UsdcToWbtc": 18742833,
    "WbtcToUsdc": 18855612,
    "UsdcToWeth": 18815625,
    "WethToUsdc": 18848579,
    "UsdcToMatic": 19647324,
    "MaticToUsdc": 19680259,
    "DaiToMatic": 19682116,
    "MaticToDai": 19681340,
    "UsdcToMkr": 19582493,
    "MkrToUsdc": 19582624,
    "DaiToMkr": 19315922,
    "MkrToDai": 19357600,
    "UsdcToIdle": 22328540,
    "UsdcToRexslpEthUsdc": 20830848,
    "UsdcToRexslpEthIdle": 23441465,
    "UsdcToRic": 20077955
}

REX_MARKET_NATIVE_TOKEN = {
    "DaiToWeth": 'ethereum',
    "WethToDai": 'dai',
    "UsdcToWbtc": 'bitcoin',
    "WbtcToUsdc": 'usd-coin',
    "UsdcToWeth": 'ethereum',
    "WethToUsdc": 'usd-coin',
    "UsdcToMatic": 'matic-network',
    "MaticToUsdc": 'usd-coin',
    "DaiToMatic": 'matic-network',
    "MaticToDai": 'dai',
    "UsdcToMkr": 'maker',
    "MkrToUsdc": 'usd-coin',
    "DaiToMkr": 'maker',
    "MkrToDai": 'dai',
    "UsdcToIdle": 'idle',
    "UsdcToRexslpEthUsdc": ('sushi', 'matic-network'),
    "UsdcToRexslpEthIdle": ('sushi', 'matic-network'),
    "UsdcToRic": 'richochet'
}

NATIVE_TOKEN_ADDRESSES = {
    'bitcoin': "0x4086eBf75233e8492F1BCDa41C7f2A8288c2fB92",
    'dai': "0x1305F6B6Df9Dc47159D12Eb7aC2804d4A33173c2",
    'ethereum': "0x27e1e4E6BC79D93032abef01025811B7E4727e85",
    'usd-coin': "0xCAa7349CEA390F89641fe306D93591f87595dc1F",
    'matic-network': "0x3aD736904E9e65189c3000c7DD2c8AC8bB7cD4e3",
    'maker': "0x2c530aF1f088B836FA0dCa23c7Ea50E669508C4C",
    'idle': "0xB63E38D21B31719e6dF314D3d2c351dF0D4a9162",
    'sushi': "0xDaB943C03f9e84795DC7BF51DdC71DaF0033382b",
    'richochet': "0x263026E7e53DBFDce5ae55Ade22493f828922965"
}

AVERAGE_GAS_PER_CONTRACT = 1500000 * 50 * 1000

FEE = .02