module State exposing (init, update, subscriptions)

import Types exposing (..)


init : Flags -> ( Model, Cmd Msg )
init flags =
    ( (Model
        flags.issue_tags
        flags.reason_tags
        flags.content_tags
        flags.issue_label
        flags.content_label
        flags.reason_label
        flags.selected_tags
        1
      )
    , Cmd.none
    )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ChangePosition newPosition ->
            ( { model | position = newPosition }, Cmd.none )

        SelectTag tag ->
            ( { model | selected_tags = update_selected model tag }, Cmd.none )


update_selected model tag =
    if List.member tag model.selected_tags then
        List.filter (\t -> t /= tag) model.selected_tags
    else
        tag :: model.selected_tags


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none
