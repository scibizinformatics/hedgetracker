const { AnyHedgeManager, isParsedMutualRedemptionData, isParsedPayoutData } = require('@generalprotocols/anyhedge');

const parse = async function(rawTxHex) {
    const manager = new AnyHedgeManager();
    const parsedPayoutData = await manager.parseSettlementTransaction(rawTxHex);
    if (isParsedPayoutData(parsedPayoutData)) {
        console.log(JSON.stringify(parsedPayoutData, null, 2));
    }
}

const fs = require('fs');
const RAW_TX_HEX = fs.readFileSync(0, 'utf-8');
parse(RAW_TX_HEX);
