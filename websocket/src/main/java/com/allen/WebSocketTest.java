package com.allen;

import java.io.IOException;
import java.util.concurrent.CopyOnWriteArraySet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import javax.websocket.*;
import javax.websocket.server.ServerEndpoint;

/**
 * @ServerEndpoint 注解是一个类层次的注解，它的功能主要是将目前的类定义成一个websocket服务器端,
 * 注解的值将被用于监听用户连接的终端访问URL地址,客户端可以通过这个URL来连接到WebSocket服务器端
 */
@ServerEndpoint("/websocket")
public class WebSocketTest {

    private static Logger logger = LoggerFactory
            .getLogger(WebSocketTest.class);

    //静态变量，用来记录当前在线连接数。应该把它设计成线程安全的。
    private static int onlineCount = 0;

    //concurrent包的线程安全Set，用来存放每个客户端对应的MyWebSocket对象。若要实现服务端与单一客户端通信的话，可以使用Map来存放，其中Key可以为用户标识
    private static CopyOnWriteArraySet<WebSocketTest> webSocketSet = new CopyOnWriteArraySet<>();

    //与某个客户端的连接会话，需要通过它来给客户端发送数据
    private Session session;

    /**
     * 连接建立成功调用的方法
     * @param session  可选的参数。session为与某个客户端的连接会话，需要通过它来给客户端发送数据
     */
    @OnOpen
    public void onOpen(Session session){
        this.session = session;
        webSocketSet.add(this);     //加入set中
        addOnlineCount();           //在线数加1
        try {
            this.sendMessage("Connect successfully");
        } catch (IOException e) {
            e.printStackTrace();
        }
        logger.info("有新连接加入！当前在线人数为" + getOnlineCount());
    }

    /**
     * 连接关闭调用的方法
     */
    @OnClose
    public void onClose(){
        webSocketSet.remove(this);  //从set中删除
        subOnlineCount();           //在线数减1
        logger.info("有一连接关闭！当前在线人数为" + getOnlineCount());
    }

    /**
     * 收到客户端消息后调用的方法
     * @param message 客户端发送过来的消息
     */
    @OnMessage
    public void onMessage(String message) throws InterruptedException {
        logger.info("来自客户端的消息:" + message);
        //群发消息
        for (WebSocketTest item : webSocketSet) {
            if (message.equals("push")){
                int count = 0;
                do {
                    try {
                        item.sendMessage("Hello WebSocket");
                        count ++;
                        Thread.sleep(1000);
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                } while (count < 10);

            }else {
                try {
                    item.sendMessage(message);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

        }
    }

    /**
     * 发生错误时调用
     * @param error
     */
    @OnError
    public void onError(Throwable error){
        logger.info("发生错误");
        error.printStackTrace();
    }

    /**
     * 这个方法与上面几个方法不一样。没有用注解，是根据自己需要添加的方法。
     * @param message
     * @throws IOException
     */
    private void sendMessage(String message) throws IOException{
        this.session.getBasicRemote().sendText(message);
        //this.session.getAsyncRemote().sendText(message);
    }

    private static synchronized int getOnlineCount() {
        return onlineCount;
    }

    private static synchronized void addOnlineCount() {
        WebSocketTest.onlineCount++;
    }

    private static synchronized void subOnlineCount() {
        WebSocketTest.onlineCount--;
    }
}