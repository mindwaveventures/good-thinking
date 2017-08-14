module State exposing (init, update, subscriptions)

import Types exposing (..)
import Rest exposing (..)


init : Flags -> ( Model, Cmd Msg )
init flags =
    update (GetData flags.query)
        (Model
            flags.issue_tags
            flags.reason_tags
            flags.content_tags
            flags.issue_label
            flags.content_label
            flags.reason_label
            flags.selected_tags
            1
            []
        )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        ChangePosition newPosition ->
            ( { model | position = newPosition }, Cmd.none )

        SelectTag tag ->
            let
                new_model =
                    { model | selected_tags = update_selected model tag }
            in
                ( new_model, getData (create_query new_model.selected_tags) )

        QueryComplete response ->
            case response of
                Ok result ->
                    ( { model | resources = result }, Cmd.none )

                Err error ->
                    ( model, Cmd.none )

        GetData url ->
            ( model, getData url )


update_selected : Model -> Tag -> List Tag
update_selected model tag =
    if List.member tag model.selected_tags then
        List.filter (\t -> t /= tag) model.selected_tags
    else
        tag :: model.selected_tags


create_query : List Tag -> String
create_query tags =
    List.foldl (\a b -> b ++ a.tag_type ++ "=" ++ a.name ++ "&") "?" tags


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none
