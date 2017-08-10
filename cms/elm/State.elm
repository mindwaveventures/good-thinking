module State exposing (init, update, subscriptions)

import Types exposing (..)


init : Flags -> ( Model, Cmd Msg )
init flags =
    ( (Model flags.issue_tags flags.reason_tags flags.content_tags 1), Cmd.none )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ChangePosition newPosition ->
            ( { model | position = newPosition }, Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none
