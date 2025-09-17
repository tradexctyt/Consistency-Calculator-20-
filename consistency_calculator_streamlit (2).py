import React, { useState } from "react";

export default function ConsistencyCalculator() {
  const [profits, setProfits] = useState([""]);

  const handleProfitChange = (index, value) => {
    const updated = [...profits];
    updated[index] = value;
    setProfits(updated);
  };

  const addDay = () => {
    setProfits([...profits, ""]);
  };

  const totalProfit = profits.reduce((sum, val) => sum + (parseFloat(val) || 0), 0);
  const biggestDay = Math.max(...profits.map(val => parseFloat(val) || 0), 0);
  const maxAllowed = totalProfit * 0.2;
  const consistent = biggestDay <= maxAllowed;

  // Calculate recommendation for next trade
  let recommendation = null;
  if (!consistent && totalProfit > 0) {
    const requiredTotal = biggestDay / 0.20;
    const needed = requiredTotal - totalProfit;
    recommendation = needed > 0 ? needed.toFixed(2) : null;
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-lg">
        <h1 className="text-2xl font-bold mb-4 text-center">20% Consistency Calculator</h1>
        <p className="mb-6 text-gray-600 text-center">
          Enter your daily profits below. The calculator will show if you meet the 20% consistency rule for withdrawals.
        </p>

        {profits.map((profit, index) => (
          <div key={index} className="mb-3">
            <label className="block text-sm font-medium text-gray-700">Day {index + 1} Profit ($)</label>
            <input
              type="number"
              value={profit}
              onChange={(e) => handleProfitChange(index, e.target.value)}
              className="mt-1 p-2 border rounded-lg w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
              placeholder="Enter profit for the day"
            />
          </div>
        ))}

        <button
          onClick={addDay}
          className="mt-2 mb-6 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg shadow"
        >
          + Add Day
        </button>

        <div className="p-4 bg-gray-50 rounded-xl shadow-inner">
          <p className="text-lg">📊 Total Profit: <strong>${totalProfit.toFixed(2)}</strong></p>
          <p className="text-lg">📈 Biggest Day Profit: <strong>${biggestDay.toFixed(2)}</strong></p>
          <p className="text-lg">✅ Max Allowed (20%): <strong>${maxAllowed.toFixed(2)}</strong></p>

          {recommendation && (
            <p className="text-lg text-yellow-600 mt-2">💡 To meet the rule, you need at least <strong>${recommendation}</strong> more profit in future trades.</p>
          )}

          <p className={`text-xl font-bold mt-4 ${consistent ? "text-green-600" : "text-red-600"}`}>
            {consistent ? "✅ Consistent — Eligible to Withdraw" : "❌ Not Consistent — Keep Trading"}
          </p>
        </div>
      </div>
    </div>
  );
}
