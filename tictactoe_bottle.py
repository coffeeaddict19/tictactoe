from bottle import default_app, post, get, request, response, template, run
import tictactoe_logic
import json
import uuid

session_dict = {}

@get('/tictactoe')
def tictactoe_get_handler():
    return template('tictactoe_page.html')

@post('/tictactoe')
def tictactoe_post_handler():
    jsonoutput = None
    try:
        # parse input data
        try:
            data = request.json
        except:
            print 'threw exception on parse'
            raise ValueError

        if data is None:
            print 'threw exception on no data recieved'
            raise ValueError
            
        print 'data', data
        if "requestType" in data:
            typeOfRequest = data["requestType"]
            if typeOfRequest == "newgame":
                sessionid = str(uuid.uuid4())
                session_dict[sessionid] = {'logic':tictactoe_logic.tictactoeGame()}
                jsonoutput = {'session_id':sessionid}
            elif typeOfRequest == "playgame":
                if "play" in data and "session_id" in data:
                    playin = data['play']
                    sessionid_in = data['session_id']
                    logic = session_dict[sessionid_in]['logic']
                    playout = logic.makeplay(playin)
                    gamestate_out = playout[0]
                    boardstate_out = playout[1]
                    jsonoutput = {'gameboard_grid_x': boardstate_out[0], 'gameboard_grid_o': boardstate_out[1], 'gameresult_end': gamestate_out}
                else:
                    raise ValueError
            else:
                raise ValueError

    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return
    
    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps(jsonoutput)
    
application = default_app()
#run(host='localhost', port=8080, debug=True)