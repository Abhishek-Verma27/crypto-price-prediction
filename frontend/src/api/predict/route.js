import { NextResponse } from 'next/server';

export async function POST(request) {
  try {
    const body = await request.json();
    const { coin, prices } = body;

    // Format the data according to your backend's expected structure
    const formattedData = [
      {
        lag_1: prices[4],
        lag_2: prices[3],
        lag_3: prices[2],
        lag_4: prices[1],
        lag_5: prices[0],
      }
    ];

    console.log('Sending to backend:', {
      url: `http://127.0.0.1:5000/predict/${coin.toLowerCase()}`,
      data: formattedData
    });

    const response = await fetch(`http://127.0.0.1:5000/predict/${coin.toLowerCase()}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formattedData),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Backend error:', errorText);
      throw new Error(`Backend error: ${response.status}`);
    }

    const data = await response.json();
    console.log('Backend response:', data);

    return NextResponse.json({
      prediction: {
        coin: coin,
        price: data.prediction,
      },
      transaction: {
        status: "success",
        hash: data.tx_hash,
      },
    });
  } catch (error) {
    console.error('Prediction error:', error);
    return NextResponse.json(
      { error: `Failed to submit prediction: ${error.message}` },
      { status: 500 }
    );
  }
}
