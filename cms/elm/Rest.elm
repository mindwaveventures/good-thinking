module Rest exposing (..)

import Types exposing (..)
import Http
import Json.Decode as Decode
import Json.Encode as Encode


getData : String -> Cmd Msg
getData query =
    Http.get ("/get_json_data" ++ query) decodeInitialData
        |> Http.send QueryComplete


decodeInitialData =
    Decode.field "resources" resourceDecoder


resourceDecoder : Decode.Decoder (List String)
resourceDecoder =
    Decode.list Decode.string
