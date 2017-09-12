module Resources.View exposing (..)

import Types exposing (..)
import State exposing (..)
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick, onCheck)
import Json.Encode


view : String -> String -> Html Msg
view page classname =
    div [ property "innerHTML" (Json.Encode.string page), class classname ] []
