const { connectLambda, getStore } = require("@netlify/blobs");

function json(statusCode, data) {
  return {
    statusCode,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store"
    },
    body: JSON.stringify(data)
  };
}

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return json(405, {
      ok: false,
      error: "Method Not Allowed"
    });
  }

  try {
    connectLambda(event);

    const body = JSON.parse(event.body || "{}");

    const name = String(body.name || "匿名").trim().slice(0, 12);
    const message = String(body.message || "").trim().slice(0, 60);

    if (!message) {
      return json(400, {
        ok: false,
        error: "留言不能为空"
      });
    }

    const store = getStore("graduation-album");
    const barrages = await store.get("barrages", { type: "json" }) || [];

    const item = {
      id: Date.now().toString() + "-" + Math.random().toString(36).slice(2),
      name,
      message,
      created_at: new Date().toISOString(),
      source: "barrage"
    };

    barrages.unshift(item);

    await store.set("barrages", JSON.stringify(barrages.slice(0, 100)), {
      contentType: "application/json"
    });

    return json(200, {
      ok: true,
      message: "弹幕发送成功",
      item
    });
  } catch (err) {
    console.error("submit-barrage error:", err);

    return json(500, {
      ok: false,
      error: err.message
    });
  }
};