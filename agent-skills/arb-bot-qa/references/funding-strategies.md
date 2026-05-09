# Funding Strategies for Triangular Arbitrage

## Overview

This guide compares different funding strategies for triangular arbitrage bots and their impact on profitability.

## Strategies

### 1. Pure Flash Loans (Current default)

**Architecture:**
```
Aave V3 Pool
    ↓ flash loan (0.09% fee)
Bot Contract
    ↓ executes 3 swaps
Profit = final_amount - (flash_amount + 0.09% fee) - gas
```

**Code Pattern:**
```javascript
const arbRoute = {
  startToken: ADDR.USDC,
  flashAmount: flashAmt,  // 100% from Aave
  hop: hops
};
```

**Pros:**
- ✅ No upfront capital required
- ✅ Unlimited capital available (pool depth dependent)
- ✅ Risk-free (if trade fails, flash loan is not executed)
- ✅ Highly scalable

**Cons:**
- ❌ 0.09% fee on every trade eats into margins
- ❌ Must wait for flash callback (adds latency)
- ❌ Limited to Aave-supported tokens

---

### 2. Hybrid Funding (Recommended)

**Architecture:**
```
Wallet Capital (no fee) + Flash Loan (0.09% fee)
    ↓
Bot Contract
    ↓ executes 3 swaps
Profit = final_amount - (flash_amount × 0.09%) - gas
```

**Code Pattern:**
```javascript
interface FundingStrategy {
  walletBufferUsd: number;      // e.g., $5,000 wallet-owned USDC
  flashLoanRatio: number;       // e.g., 0.5 = 50% flash, 50% self-funded
  minWalletReserve: number;     // Keep minimum in wallet (e.g., $1,000)
}

async function calculateOptimalFunding(
  targetAmountUsd: number,
  strategy: FundingStrategy
): Promise<{ walletAmount: BigInt; flashAmount: BigInt; }> {
  const token = new ethers.Contract(startToken, ERC20_BALANCE_ABI, provider);
  const walletBalance = await token.balanceOf(wallet.address);
  const walletBalanceUsd = Number(walletBalance) / 10**decimals;

  const availableWalletUsd = Math.max(
    walletBalanceUsd - strategy.minWalletReserve,
    0
  );

  const walletShare = Math.min(
    availableWalletUsd,
    targetAmountUsd * strategy.flashLoanRatio
  );

  const flashShare = targetAmountUsd - walletShare;

  const walletAmount = ethers.parseUnits(walletShare.toFixed(decimals), decimals);
  const flashAmount = ethers.parseUnits(flashShare.toFixed(decimals), decimals);

  return { walletAmount, flashAmount };
}

const arbRoute = {
  startToken,
  selfFundedAmount: funding.walletAmount,
  flashAmount: funding.flashAmount,
  hop: hops
};
```

**Pros:**
- ✅ Reduces Aave fee exposure (only pay on flash portion)
- ✅ Faster execution (no flash callback for self-funded portion)
- ✅ Increased capital efficiency (wallet + flash)
- ✅ Can execute when Aave is congested

**Cons:**
- ❌ Requires upfront wallet capital
- ❌ Capital locked in wallet reduces flexibility

**Recommended Parameters:**
- **Ethereum:** 40% wallet + 60% flash (higher gas costs → more wallet usage beneficial)
- **Arbitrum:** 30% wallet + 70% flash (lower gas costs -> can use more flash)

---

### 3. Pure Wallet Funding (Not recommended)

**Architecture:**
```
Wallet balances
    ↓
Bot Contract
    ↓ executes 3 swaps
Profit = final_amount - initial_amount - gas
```

**Code Pattern:**
```javascript
const startTokenBalance = ethers.parseUnits("10000", 6);  // $10k from wallet
const arbRoute = {
  startToken,
  flashAmount: startTokenBalance,
  selfFundedAmount: ethers.ZeroAddress,  // No flash loan
  hop: hops
};
```

**Pros:**
- ✅ No Aave fee (0.09% saved every trade)
- ✅ Fastest execution (no flash loan overhead)

**Cons:**
- ❌ Requires significant upfront capital
- ❌ Unlimited capital not available
- ❌ Opportunity cost of capital

**Cost Comparison ($10k trade):**

| Strategy | Aave Fee | Gas Cost | Net Profit (at $50 gross) |
|----------|----------|----------|---------------------------|
| Pure Flash | $9.00 | $2.00 (ETH) / $0.10 (ARB) | $39.00 (ETH) / $40.90 (ARB) |
| Hybrid (40/60) | $5.40 | $2.00 (ETH) / $0.10 (ARB) | $42.60 (ETH) / $44.50 (ARB) |
| Pure Wallet | $0.00 | $2.00 (ETH) / $0.10 (ARB) | $48.00 (ETH) / $49.90 (ARB) |

**Savings vs Pure Flash:**
- Hybrid: +$3.60 per trade (8.8-9.2% improvement)
- Pure Wallet: +$9.00 per trade (23% improvement)

---

## Decision Matrix

### When to use each strategy

**Pure Flash:**
- Starting with no capital
- Testing new strategies
- When capital availability is primary constraint
- When Aave fees are acceptable

**Hybrid Funding (Recommended):**
- Has some wallet capital ($5k-$25k)
- Wants to reduce Aave fee exposure
- Ethereum environment (high gas makes fee savings valuable)
- Sustainable long-term operations

**Pure Wallet:**
- Has substantial capital ($100k+)
- Maximum profitability is priority
- Comfortable with capital opportunity cost

---

## Implementation Considerations

### Flash Loan Ratio Optimization

The optimal flash loan ratio depends on:
- Network gas costs (higher gas → more wallet buffer helps)
- Risk tolerance (more wallet = more capital at risk)
- Capital availability
- Aave congestion levels

### Risk Management

With hybrid funding:
- Only the flash loan portion is risk-free
- Wallet capital is at risk if trade fails
- Consider adding circuit breakers for consecutive failures

### Profit Compounding

Profits can be automatically reinvested to grow wallet capital over time:
```javascript
interface CompoundingConfig {
  enabled: boolean;
  targetWalletBalance: number;   // e.g., $50,000
  reinvestThreshold: number;     // e.g., $1,000
  maxReinvestRatio: number;      // e.g., 0.15 = 15%
}
```

---

## Network-Specific Guidance

### Ethereum Mainnet

**Characteristics:**
- High gas costs ($2-5 typical per trade)
- Flashbots Protect for MEV protection
- 21 triangular routes (includes FRAX)

**Recommended Strategy:** Hybrid 40/60
- Higher gas costs make fee savings more valuable
- $9-15 savings per trade is significant

### Arbitrum

**Characteristics:**
- Low gas costs ($0.05-0.15 typical per trade)
- 22 triangular routes
- No MEV concerns typically

**Recommended Strategy:** Hybrid 30/70 or Pure Flash
- Lower gas costs reduce fee impact
- Can use more flash while still profitable

---

## Code Examples

### Adding Hybrid Funding to Existing Bot

1. Update bot contract to accept self-funded amounts
2. Modify scanner to calculate optimal funding split
3. Update executeArbitrage() to use hybrid amounts
4. Add wallet balance checking before each run

See bot scanner QA reports for complete implementation examples.
