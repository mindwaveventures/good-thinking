module Rest exposing (..)

import Types exposing (..)
import Http
import Json.Decode as Decode
import Json.Encode as Encode


getData : String -> (Result Http.Error Results -> Msg) -> Cmd Msg
getData query msg =
    Http.get ("/get_json_data" ++ query) decodeInitialData
        |> Http.send msg


decodeInitialData =
    Decode.map3 Results
        (Decode.field "resources" resourceDecoder)
        (Decode.field "resource_count" Decode.int)
        (Decode.field "tips" resourceDecoder)


resourceDecoder : Decode.Decoder (List String)
resourceDecoder =
    Decode.list Decode.string
